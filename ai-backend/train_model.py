#!/usr/bin/env python3
"""
Training script for AI Disease Detection models

This script trains disease classification models on medical image datasets.
For production use, train on properly licensed medical datasets.

Usage:
    python train_model.py --data_dir /path/to/data --model_type chest_xray --epochs 50
"""

import argparse
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import numpy as np
from tqdm import tqdm
import logging
from datetime import datetime

from app.models.model_loader import DiseaseClassifier
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalImageDataset(Dataset):
    """Custom dataset for medical images"""
    
    def __init__(self, data_dir: str, transform=None):
        """
        Args:
            data_dir: Directory with class subdirectories containing images
            transform: Optional transform to apply
        """
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        self.classes = []
        
        # Load samples from directory structure
        # Expected: data_dir/class_name/image.jpg
        for class_idx, class_name in enumerate(sorted(os.listdir(data_dir))):
            class_path = os.path.join(data_dir, class_name)
            if os.path.isdir(class_path):
                self.classes.append(class_name)
                for img_name in os.listdir(class_path):
                    if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        self.samples.append((
                            os.path.join(class_path, img_name),
                            class_idx
                        ))
        
        logger.info(f"Loaded {len(self.samples)} samples from {len(self.classes)} classes")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
        
        return image, label


def get_transforms(training: bool = True):
    """Get image transforms for training or validation"""
    if training:
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc="Training")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({
            'loss': f'{running_loss/total:.4f}',
            'acc': f'{100.*correct/total:.2f}%'
        })
    
    return running_loss / len(dataloader), correct / total


def validate(model, dataloader, criterion, device):
    """Validate the model"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in tqdm(dataloader, desc="Validating"):
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return running_loss / len(dataloader), correct / total


def train_model(
    data_dir: str,
    model_type: str,
    epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    val_split: float = 0.2
):
    """
    Train a disease classification model
    
    Args:
        data_dir: Path to training data (class subdirectories)
        model_type: Type of model (chest_xray, bone_xray, skin_image)
        epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Initial learning rate
        val_split: Validation split ratio
    """
    logger.info(f"Starting training for {model_type}")
    logger.info(f"Data directory: {data_dir}")
    
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Load dataset
    train_transform = get_transforms(training=True)
    val_transform = get_transforms(training=False)
    
    full_dataset = MedicalImageDataset(data_dir, transform=train_transform)
    num_classes = len(full_dataset.classes)
    
    logger.info(f"Classes: {full_dataset.classes}")
    logger.info(f"Number of classes: {num_classes}")
    
    # Split dataset
    val_size = int(len(full_dataset) * val_split)
    train_size = len(full_dataset) - val_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, val_size]
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=4
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False, num_workers=4
    )
    
    logger.info(f"Training samples: {len(train_dataset)}")
    logger.info(f"Validation samples: {len(val_dataset)}")
    
    # Create model
    model = DiseaseClassifier(num_classes=num_classes)
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5
    )
    
    # Training loop
    best_val_acc = 0.0
    best_model_path = None
    
    for epoch in range(epochs):
        logger.info(f"\nEpoch {epoch+1}/{epochs}")
        logger.info("-" * 40)
        
        # Train
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device
        )
        
        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        # Update scheduler
        scheduler.step(val_loss)
        
        logger.info(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
        logger.info(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_path = os.path.join(
                settings.MODEL_PATH,
                f"{model_type}.pth"
            )
            torch.save(model.state_dict(), best_model_path)
            logger.info(f"Saved best model to {best_model_path}")
    
    logger.info(f"\nTraining complete!")
    logger.info(f"Best validation accuracy: {best_val_acc:.4f}")
    logger.info(f"Model saved to: {best_model_path}")
    
    return best_model_path, best_val_acc


def main():
    parser = argparse.ArgumentParser(description="Train AI Disease Detection models")
    
    parser.add_argument(
        "--data_dir", type=str, required=True,
        help="Path to training data directory"
    )
    parser.add_argument(
        "--model_type", type=str, required=True,
        choices=["chest_xray", "bone_xray", "skin_image"],
        help="Type of model to train"
    )
    parser.add_argument(
        "--epochs", type=int, default=50,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch_size", type=int, default=32,
        help="Batch size for training"
    )
    parser.add_argument(
        "--learning_rate", type=float, default=0.001,
        help="Initial learning rate"
    )
    parser.add_argument(
        "--val_split", type=float, default=0.2,
        help="Validation split ratio"
    )
    
    args = parser.parse_args()
    
    # Ensure models directory exists
    os.makedirs(settings.MODEL_PATH, exist_ok=True)
    
    # Train model
    train_model(
        data_dir=args.data_dir,
        model_type=args.model_type,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        val_split=args.val_split
    )


if __name__ == "__main__":
    main()
