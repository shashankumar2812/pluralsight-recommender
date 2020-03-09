import tensorflow as tf
from paths import model_checkpoint_file, model_train_log_file
from .model_config import sim_course_level_model_params


class TrainStopCallback(tf.keras.callbacks.Callback):
    def __init__(self, expected_accuracy):
        self.expected_accuracy = expected_accuracy

    def on_epoch_end(self, epoch, logs={}):
        if logs.get("accuracy") > self.expected_accuracy:
            print(
                f"\n Training will stop because expected training accuracy {self.expected_accuracy} is acheived"
            )
            self.model.stop_training = True


class ModelCheckPoint:
    def save(self, checkpoint_path):
        model_cp_callback = tf.keras.callbacks.ModelCheckpoint(
            model_checkpoint_file, monitor="val_loss", save_best_only=True
        )
        return model_cp_callback


train_stop_callback = TrainStopCallback(
    expected_accuracy=sim_course_level_model_params[
        "training_stop_accuracy_threshold_callback"
    ]
)
cp_callback = ModelCheckPoint().save(model_checkpoint_file)
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=model_train_log_file, histogram_freq=1
)
