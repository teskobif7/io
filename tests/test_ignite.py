# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
# ==============================================================================
"""Tests for IGFS."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from tensorflow.python.platform import test
from tensorflow_io.ignite import IgniteDataset
from tensorflow.data import Dataset
from tensorflow.python.client import session
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import errors
import tensorflow_io.ignite.python.ops.igfs_ops  # pylint: disable=unused-import
from tensorflow.python.platform import gfile


class IGFSTest(test.TestCase):
  """The Apache Ignite servers have to setup before the test and tear down

     after the test manually. The docker engine has to be installed.

     To setup Apache Ignite servers:
     $ bash start_ignite.sh

     To tear down Apache Ignite servers:
     $ bash stop_ignite.sh
  """

  def test_create_file(self):
    """Test create file.

    """
    # Setup and check preconditions.
    file_name = "igfs:///test_create_file/1"
    self.assertFalse(gfile.Exists(file_name))
    # Create file.
    with gfile.Open(file_name, mode="w") as w:
      w.write("")
    # Check that file was created.
    self.assertTrue(gfile.Exists(file_name))
    # Remove file.
    gfile.Remove(file_name)
    # Check that file was removed.
    self.assertFalse(gfile.Exists(file_name))

  def test_write_read_file(self):
    """Test write/read file.

    """
    # Setup and check preconditions.
    file_name = "igfs:///test_write_read_file/1"
    rows = 10000
    self.assertFalse(gfile.Exists(file_name))
    # Write data.
    with gfile.Open(file_name, mode="w") as w:
      for i in range(rows):
        w.write("This is row\n")
    # Read data.
    with gfile.Open(file_name, mode="r") as r:
      lines = r.readlines()
    # Check that data is equal.
    self.assertEqual(rows, len(lines))
    for i in range(rows):
      self.assertEqual("This is row\n", lines[i])
    # Remove file.
    gfile.Remove(file_name)
    # Check that file was removed.
    self.assertFalse(gfile.Exists(file_name))

  def test_delete_recursively(self):
    """Test delete recursively.

    """
    # Setup and check preconditions.
    dir_name = "igfs:///test_delete_recursively/"
    file_name = "igfs:///test_delete_recursively/1"
    self.assertFalse(gfile.Exists(dir_name))
    self.assertFalse(gfile.Exists(file_name))
    gfile.MkDir(dir_name)
    with gfile.Open(file_name, mode="w") as w:
      w.write("")
    self.assertTrue(gfile.Exists(dir_name))
    self.assertTrue(gfile.Exists(file_name))
    # Delete directory recursively.
    gfile.DeleteRecursively(dir_name)
    # Check that directory was deleted.
    self.assertFalse(gfile.Exists(dir_name))
    self.assertFalse(gfile.Exists(file_name))

  def test_copy(self):
    """Test copy.

    """
    # Setup and check preconditions.
    src_file_name = "igfs:///test_copy/1"
    dst_file_name = "igfs:///test_copy/2"
    self.assertFalse(gfile.Exists(src_file_name))
    self.assertFalse(gfile.Exists(dst_file_name))
    with gfile.Open(src_file_name, mode="w") as w:
      w.write("42")
    self.assertTrue(gfile.Exists(src_file_name))
    self.assertFalse(gfile.Exists(dst_file_name))
    # Copy file.
    gfile.Copy(src_file_name, dst_file_name)
    # Check that files are identical.
    self.assertTrue(gfile.Exists(src_file_name))
    self.assertTrue(gfile.Exists(dst_file_name))
    with gfile.Open(dst_file_name, mode="r") as r:
      data = r.read()
    self.assertEqual("42", data)
    # Remove file.
    gfile.Remove(src_file_name)
    gfile.Remove(dst_file_name)
    # Check that file was removed.
    self.assertFalse(gfile.Exists(src_file_name))
    self.assertFalse(gfile.Exists(dst_file_name))

  def test_is_directory(self):
    """Test is directory.

    """
    # Setup and check preconditions.
    dir_name = "igfs:///test_is_directory/1"
    file_name = "igfs:///test_is_directory/2"
    with gfile.Open(file_name, mode="w") as w:
      w.write("")
    gfile.MkDir(dir_name)
    # Check that directory is a directory.
    self.assertTrue(gfile.IsDirectory(dir_name))
    # Check that file is not a directory.
    self.assertFalse(gfile.IsDirectory(file_name))

  def test_list_directory(self):
    """Test list directory.

    """
    # Setup and check preconditions.
    dir_name = "igfs:///test_list_directory/"
    file_names = [
        "igfs:///test_list_directory/1", "igfs:///test_list_directory/2/3"
    ]
    ch_dir_names = [
        "igfs:///test_list_directory/4",
    ]
    for file_name in file_names:
      with gfile.Open(file_name, mode="w") as w:
        w.write("")
    for ch_dir_name in ch_dir_names:
      gfile.MkDir(ch_dir_name)
    ls_expected_result = file_names + ch_dir_names
    # Get list of files in directory.
    ls_result = gfile.ListDirectory(dir_name)
    # Check that list of files is correct.
    self.assertEqual(len(ls_expected_result), len(ls_result))
    for e in ["1", "2", "4"]:
      self.assertTrue(e in ls_result)

  def test_make_dirs(self):
    """Test make dirs.

    """
    # Setup and check preconditions.
    dir_name = "igfs:///test_make_dirs/"
    self.assertFalse(gfile.Exists(dir_name))
    # Make directory.
    gfile.MkDir(dir_name)
    # Check that directory was created.
    self.assertTrue(gfile.Exists(dir_name))
    # Remove directory.
    gfile.Remove(dir_name)
    # Check that directory was removed.
    self.assertFalse(gfile.Exists(dir_name))

  def test_remove(self):
    """Test remove.

    """
    # Setup and check preconditions.
    file_name = "igfs:///test_remove/1"
    self.assertFalse(gfile.Exists(file_name))
    with gfile.Open(file_name, mode="w") as w:
      w.write("")
    self.assertTrue(gfile.Exists(file_name))
    # Remove file.
    gfile.Remove(file_name)
    # Check that file was removed.
    self.assertFalse(gfile.Exists(file_name))

  def test_rename_file(self):
    """Test rename file.

    """
    # Setup and check preconditions.
    src_file_name = "igfs:///test_rename_file/1"
    dst_file_name = "igfs:///test_rename_file/2"
    with gfile.Open(src_file_name, mode="w") as w:
      w.write("42")
    self.assertTrue(gfile.Exists(src_file_name))
    # Rename file.
    gfile.Rename(src_file_name, dst_file_name)
    # Check that only new name of file is available.
    self.assertFalse(gfile.Exists(src_file_name))
    self.assertTrue(gfile.Exists(dst_file_name))
    with gfile.Open(dst_file_name, mode="r") as r:
      data = r.read()
    self.assertEqual("42", data)
    # Remove file.
    gfile.Remove(dst_file_name)
    # Check that file was removed.
    self.assertFalse(gfile.Exists(dst_file_name))

  def test_rename_dir(self):
    """Test rename dir.

    """
    # Setup and check preconditions.
    src_dir_name = "igfs:///test_rename_dir/1"
    dst_dir_name = "igfs:///test_rename_dir/2"
    gfile.MkDir(src_dir_name)
    # Rename directory.
    gfile.Rename(src_dir_name, dst_dir_name)
    # Check that only new name of directory is available.
    self.assertFalse(gfile.Exists(src_dir_name))
    self.assertTrue(gfile.Exists(dst_dir_name))
    self.assertTrue(gfile.IsDirectory(dst_dir_name))
    # Remove directory.
    gfile.Remove(dst_dir_name)
    # Check that directory was removed.
    self.assertFalse(gfile.Exists(dst_dir_name))


class IgniteDatasetTest(test.TestCase):
  """The Apache Ignite servers have to setup before the test and tear down

     after the test manually. The docker engine has to be installed.

     To setup Apache Ignite servers:
     $ bash start_ignite.sh

     To tear down Apache Ignite servers:
     $ bash stop_ignite.sh
  """

  def test_ignite_dataset_with_plain_client(self):
    """Test Ignite Dataset with plain client.

    """
    self._clear_env()
    ds = IgniteDataset(cache_name="SQL_PUBLIC_TEST_CACHE", port=42300)
    self._check_dataset(ds)

  def test_ignite_dataset_with_plain_client_with_interleave(self):
    """Test Ignite Dataset with plain client with interleave.

    """
    self._clear_env()
    ds = Dataset.from_tensor_slices(["localhost"]).interleave(
        lambda host: IgniteDataset(cache_name="SQL_PUBLIC_TEST_CACHE",
                                   schema_host="localhost", host=host,
                                   port=42300), cycle_length=4, block_length=16
    )
    self._check_dataset(ds)

  def _clear_env(self):
    """Clears environment variables used by Ignite Dataset.

    """
    if "IGNITE_DATASET_USERNAME" in os.environ:
      del os.environ["IGNITE_DATASET_USERNAME"]
    if "IGNITE_DATASET_PASSWORD" in os.environ:
      del os.environ["IGNITE_DATASET_PASSWORD"]
    if "IGNITE_DATASET_CERTFILE" in os.environ:
      del os.environ["IGNITE_DATASET_CERTFILE"]
    if "IGNITE_DATASET_CERT_PASSWORD" in os.environ:
      del os.environ["IGNITE_DATASET_CERT_PASSWORD"]

  def _check_dataset(self, dataset):
    """Checks that dataset provides correct data."""
    self.assertEqual(dtypes.int64, dataset.output_types["key"])
    self.assertEqual(dtypes.string, dataset.output_types["val"]["NAME"])
    self.assertEqual(dtypes.int64, dataset.output_types["val"]["VAL"])

    it = dataset.make_one_shot_iterator()
    ne = it.get_next()

    with session.Session() as sess:
      rows = [sess.run(ne), sess.run(ne), sess.run(ne)]
      with self.assertRaises(errors.OutOfRangeError):
        sess.run(ne)

    self.assertEqual({"key": 1, "val": {"NAME": b"TEST1", "VAL": 42}}, rows[0])
    self.assertEqual({"key": 2, "val": {"NAME": b"TEST2", "VAL": 43}}, rows[1])
    self.assertEqual({"key": 3, "val": {"NAME": b"TEST3", "VAL": 44}}, rows[2])


if __name__ == "__main__":
  test.main()
