import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib

class Actor():
	def __init__(self, action_dof, LEARNING_RATE=0.01):
		self.model_params = {'learning_rate':LEARNING_RATE}
		self.DNN = tf.contrib.learn.Estimator(model_fn=self.model_fn, params=self.model_params)
		self.action_dof = action_dof

	def fit(x, y, steps):
		self.DNN.fit(x=x, y=y, steps=steps)
		
	def evaluate(x, y):
		evaluation = self.DNN.evaluate(x=x, y=y, steps=1)
		return evaluation["loss"], evaluation["rmse"]

	def predict(x):
		predictions = self.DNN.predict(x=x, as_iterable=True)

	def model_fn(features, targets, mode, params):
		"""Model function for Estimator."""
		# Connect the first hidden layer to input layer
		# (features) with relu activation
		first_hidden_layer = tf.contrib.layers.relu(features, 500)

		# Connect the second hidden layer to first hidden layer with relu
		second_hidden_layer = tf.contrib.layers.relu(first_hidden_layer, 50)

		# Connect the third hidden layer to second hidden layer (no activation function)
		third_hidden_layer = tf.contrib.layers.linear(second_hidden_layer, 25)

		# Connect the output layer to third hidden layer (no activation function)
		output_layer = tf.contrib.layers.linear(third_hidden_layer, self.action_dof)

		# Reshape output layer to 1-dim Tensor to return predictions
		#predictions = tf.reshape(output_layer, [-])
		#predictions_dict = {"ages": predictions}
		predictions = output_layer

		predictions_dict = {}

		for action_iterator in range(action_dof):
			predictions_dict[str(action_iterator)] = predictions[action_iterator]

		# Calculate loss using mean squared error
		loss = -tf.log(predictions) * target

		# Calculate root mean squared error as additional eval metric
		eval_metric_ops = {
		"rmse": 0.0
		}

		train_op = tf.contrib.layers.optimize_loss(
		loss=loss,
		global_step=tf.contrib.framework.get_global_step(),
		learning_rate=params["learning_rate"],
		optimizer="SGD")

		return model_fn_lib.ModelFnOps(
		mode=mode,
		predictions=predictions_dict,
		loss=loss,
		train_op=train_op,
		eval_metric_ops=eval_metric_ops)