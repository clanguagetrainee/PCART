import tensorflow as tf
tf.contrib.data.make_csv_dataset('/home/zhang/Packages/tensorflow_file/dev.csv', 1, column_names=None, column_defaults=None, label_name=None, field_delim=',', use_quote_delim=True, na_value='', header=True, num_epochs=None, shuffle=True, shuffle_buffer_size=1, shuffle_seed=None, prefetch_buffer_size=1, num_parallel_reads=1, num_parallel_parser_calls=2, sloppy=False, default_float_type=tf.float32, num_rows_for_inference=1, select_columns=None)