NUMERIC_FEATURES=['lines_added','lines_deleted','total_changes','files_changed','commits','average_changes_per_file','source_files_changed','test_files_changed','documentation_files_changed','configuration_files_changed','number_of_file_types','test_to_source_ratio','documentation_ratio']
CATEGORICAL_FEATURES=['pr_size_category']
FEATURE_COLUMNS=NUMERIC_FEATURES+CATEGORICAL_FEATURES
TARGET_COLUMN='is_risky'
