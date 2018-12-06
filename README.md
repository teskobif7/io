# TensorFlow I/O

TensorFlow I/O is a collection of file systems and file formats that are not
available in TensorFlow's built-in support.

## Developing

The TensorFlow I/O package (`tensorflow-io`) could be built from source:
```sh
$ docker run -it tensorflow/tensorflow:custom-op /bin/bash
$ # In docker
$ ./configure.sh
$  bazel build build_pip_pkg
$  bazel-bin/build_pip_pkg artifacts
```

## License

[Apache License 2.0](LICENSE)
