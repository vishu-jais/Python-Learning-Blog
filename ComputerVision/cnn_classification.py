"""Minimal CNN template (optional - requires tensorflow)."""
from utils.common_imports import np
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
except Exception:
    tf = None
def build_simple_cnn(input_shape=(32,32,3), num_classes=10):
    if tf is None:
        raise ImportError('TensorFlow required for CNN example. Install with `pip install tensorflow`')
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Conv2D(32,3, activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(64,3, activation='relu'),
        layers.MaxPool2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
if __name__=='__main__':
    print('This module provides a CNN builder. Import and use in training script.')