from io import StringIO
import streamlit as st
import json

from processing.parser import BTParser

def upload_file(label, file_types, parser_fn, key=None, allow_multiple=False):
    """
    Upload and parse one or multiple files.

    Args:
        label (str): The label to display above the uploader.
        file_types (list): List of allowed file extensions (e.g., ["csv", "xlsx"]).
        parser_fn (function): A function that parses the uploaded file(s).
        key (str, optional): Streamlit widget key.
        allow_multiple (bool, optional): If True, allows multiple file uploads.

    Returns:
        Parsed data or list of parsed data, depending on allow_multiple.
    """
    uploaded_files = st.file_uploader(label, type=file_types, key=key, accept_multiple_files=allow_multiple)

    if uploaded_files:
        if not isinstance(uploaded_files, list):
            uploaded_files = [uploaded_files] 

        parsed_data = []
        for file_obj in uploaded_files:
            try:
                parsed = parser_fn(file_obj)
                if allow_multiple:
                    parsed_data.extend(parsed)
                else:
                    parsed_data.append(parsed)
            except Exception as e:
                st.error(f"⚠️ Error processing file '{file_obj.name}': {e}")
        
        if parsed_data:
            st.success(f"✅ Successfully uploaded {len(uploaded_files)} file(s).")
            return parsed_data if allow_multiple else parsed_data[0]
        else:
            st.error("⚠️ No valid files uploaded.")
            return None

    return None

# Helper functions
def parse_transactions(file_obj):
    # TODO: Support different statements formats
    data = BTParser().parse(file_obj, substrings_to_remove=[], sep=",")
    return data

def parse_json(file_obj):
    string_data = StringIO(file_obj.getvalue().decode("utf-8"))
    return json.load(string_data)