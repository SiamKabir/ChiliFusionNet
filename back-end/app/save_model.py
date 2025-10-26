# import tensorflow as tf
# from keras import Input, Model
# from keras.applications import EfficientNetB3

# tf.keras.backend.clear_session()
# tf.keras.backend.set_image_data_format("channels_last")

# def build_model():
#     base = EfficientNetB3(weights="imagenet", include_top=False, pooling="avg")

#     inp = Input(shape=(224, 224, 3), name="img_rgb_224")  # must be 3 channels
#     out = base(inp)
#     model = Model(inp, out, name="efficientnet_b3_feat")
#     return model

# model = build_model()
# print("Input shape:", model.input_shape)
# print("stem_conv kernel:", model.get_layer("stem_conv").get_weights()[0].shape)
