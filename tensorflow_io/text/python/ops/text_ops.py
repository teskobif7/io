# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
"""TextInput/TextOutput."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow
from tensorflow import dtypes
from tensorflow.compat.v1 import data
from tensorflow_io import _load_library
text_ops = _load_library('_text_ops.so')

class TextDataset(data.Dataset):
  """A Text Dataset
  """

  def __init__(self, filename):
    """Create a Text Reader.

    Args:
      filename: A `tf.string` tensor containing one or more filenames.
    """
    self._data_input = text_ops.text_input(filename, ["none", "gz"])
    super(TextDataset, self).__init__()

  def _inputs(self):
    return []

  def _as_variant_tensor(self):
    return text_ops.text_dataset(
        self._data_input,
        output_types=self.output_types,
        output_shapes=self.output_shapes)

  @property
  def output_shapes(self):
    return tuple([tensorflow.TensorShape([])])

  @property
  def output_classes(self):
    return tensorflow.Tensor

  @property
  def output_types(self):
    return tuple([dtypes.string])

class TextOutputSequence(object):
  """TextOutputSequence"""

  def __init__(self, filenames):
    """Create a `TextOutputSequence`.
    """
    self._filenames = filenames
    self._resource = text_ops.text_output_sequence(destination=filenames)

  def setitem(self, index, item):
    text_ops.text_output_sequence_set_item(self._resource, index, item)
