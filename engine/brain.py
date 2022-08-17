import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


def little_brain(conv_size, conv_depth):
    board3d = tf.keras.layers.Input(shape=(14, 8, 8))
    # adding the convolutional layers
    DataSet = board3d
    #for _ in range(conv_depth):
        #DataSet = tf.keras.layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', data_format='channels_first')(DataSet)
    DataSet = tf.keras.layers.Flatten()(DataSet)
    DataSet = tf.keras.layers.Dense(64, 'relu')(DataSet)
    DataSet = tf.keras.layers.Dense(1, 'sigmoid')(DataSet)
    return tf.keras.models.Model(inputs=board3d, outputs=DataSet)
  
model = little_brain(32, 4)

def load_data():
    container = np.load('-----------------.---')
    b, v = container['b'], container['v']
    v = np.asarray(v / abs(v).max() / 2 + 0.5, dtype=np.float32) # normalization (0 - 1)
    return b, v

x_train, y_train = load_data()
print(x_train.shape)
print(y_train.shape)
print(model)

model.compile(optimizer=tf.keras.optimizers.Adam(5e-4), loss='mean_squared_error')
model.summary()
model.fit(x_train, y_train,
          batch_size=2048,
          epochs=1000,
          verbose=1,
          validation_split=0.1,
          callbacks=[tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                     tf.keras.callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4)])

model.save('model.h5')