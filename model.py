import tensorflow as tf
from tensorflow import keras

import tensorflow as tf
from tensorflow import keras


class CNN:
    def __init__(self):
        self.model = self._create_model()
        self.checkpoint_path = "model_checkpoint.ckpt"
        self.checkpoint_callback = keras.callbacks.ModelCheckpoint(
            self.checkpoint_path, save_weights_only=True, save_best_only=True, monitor='val_loss', mode='min', verbose=1
        )

    def _create_model(self):
        model = keras.Sequential()

        # Convolutional layers
        model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(None, None, 3)))
        model.add(keras.layers.MaxPooling2D((2, 2)))

        model.add(keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
        model.add(keras.layers.MaxPooling2D((2, 2)))

        model.add(keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
        model.add(keras.layers.MaxPooling2D((2, 2)))

        # Flatten the output of the convolutional layers
        model.add(keras.layers.Flatten())

        # Dense layers
        model.add(keras.layers.Dense(512, activation='relu'))
        model.add(keras.layers.Dense(64 * 64, activation='sigmoid'))

        # Reshape the output to a 64x64 matrix
        model.add(keras.layers.Reshape((64, 64)))

        return model

    def train(self, x_train, y_train, x_val, y_val, epochs=10):
        self.model.compile(optimizer='adam', loss='binary_crossentropy')
        self.model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=epochs,
                       callbacks=[self.checkpoint_callback])

    def save_model(self):
        self.model.save(self.checkpoint_path)

    def load_model(self):
        self.model = keras.models.load_model(self.checkpoint_path)


if __name__ == '__main__':
    cnn = CNN()
    cnn.train(x_train, y_train, x_val, y_val, epochs=10)
    cnn.save_model()
    cnn.load_model()
