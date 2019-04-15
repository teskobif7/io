# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""MNIST Dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow
from tensorflow import dtypes
from tensorflow.compat.v1 import data
from tensorflow_io import _load_library
mnist_ops = _load_library('_mnist_ops.so')

class _MNISTBaseDataset(data.Dataset):
  """A MNIST Dataset
  """

  def __init__(self, mnist_op_class):
    """Create a MNISTReader.

    Args:
      mnist_op_class: The op of the dataset, either
          mnist_ops.mnist_image_dataset or mnist_ops.mnist_label_dataset.
      filenames: A `tf.string` tensor containing one or more filenames.
    """
    self._func = mnist_op_class
    super(_MNISTBaseDataset, self).__init__()

  def _inputs(self):
    return []

  def _as_variant_tensor(self):
    return self._func(
        self._data_input,
        output_types=self.output_types,
        output_shapes=self.output_shapes)

  @property
  def output_classes(self):
    return tensorflow.Tensor

  @property
  def output_types(self):
    return tuple([dtypes.uint8])

class MNISTImageDataset(_MNISTBaseDataset):
  """A MNIST Image Dataset
  """

  def __init__(self, filename):
    """Create a MNISTReader.

    Args:
      filenames: A `tf.string` tensor containing one or more filenames.
    """
    self._data_input = mnist_ops.mnist_image_input(filename, ["none", "gz"])
    super(MNISTImageDataset, self).__init__(
        mnist_ops.mnist_image_dataset)

  @property
  def output_shapes(self):
    return tuple([tensorflow.TensorShape([None, None])])


class MNISTLabelDataset(_MNISTBaseDataset):
  """A MNIST Label Dataset
  """

  def __init__(self, filename):
    """Create a MNISTReader.

    Args:
      filenames: A `tf.string` tensor containing one or more filenames.
    """
    self._data_input = mnist_ops.mnist_label_input(filename, ["none", "gz"])
    super(MNISTLabelDataset, self).__init__(
        mnist_ops.mnist_label_dataset)

  @property
  def output_shapes(self):
    return tuple([tensorflow.TensorShape([])])

class MNISTDataset(data.Dataset):
  """A MNIST Dataset
  """

  def __init__(self, image, label):
    """Create a MNISTReader.

    Args:
      image: A `tf.string` tensor containing image filename.
      label: A `tf.string` tensor containing label filename.
    """
    self._image = image
    self._label = label
    super(MNISTDataset, self).__init__()

  def _inputs(self):
    return []

  def _as_variant_tensor(self):
    return data.Dataset.zip( # pylint: disable=protected-access
        (MNISTImageDataset(self._image),
         MNISTLabelDataset(self._label))
        )._as_variant_tensor()

  @property
  def output_shapes(self):
    return  (tensorflow.TensorShape([None, None]), tensorflow.TensorShape([]))

  @property
  def output_classes(self):
    return tensorflow.Tensor, tensorflow.Tensor

  @property
  def output_types(self):
    return dtypes.uint8, dtypes.uint8
