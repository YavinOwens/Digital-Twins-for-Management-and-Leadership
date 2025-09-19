# Streamlit Key Parameter Guide

This guide explains which Streamlit elements support the `key` parameter and how to properly handle duplicate element ID errors.

## Elements That Support `key` Parameter

These elements support the `key` parameter and should be used when you need to prevent duplicate ID errors:

### Input Widgets
- `st.text_input()` - Text input fields
- `st.text_area()` - Multi-line text areas
- `st.number_input()` - Number input fields
- `st.selectbox()` - Dropdown select boxes
- `st.multiselect()` - Multi-select dropdowns
- `st.radio()` - Radio button groups
- `st.checkbox()` - Checkboxes
- `st.slider()` - Sliders
- `st.select_slider()` - Select sliders
- `st.date_input()` - Date pickers
- `st.time_input()` - Time pickers
- `st.file_uploader()` - File upload widgets
- `st.color_picker()` - Color pickers

### Interactive Elements
- `st.button()` - Buttons
- `st.download_button()` - Download buttons
- `st.form_submit_button()` - Form submit buttons

### Layout Elements
- `st.expander()` - Expandable sections
- `st.tabs()` - Tab containers

### Data Display Elements
- `st.dataframe()` - Data tables
- `st.table()` - Static tables
- `st.json()` - JSON display
- `st.code()` - Code blocks

### Media Elements
- `st.image()` - Images
- `st.video()` - Videos
- `st.audio()` - Audio files

## Elements That DON'T Support `key` Parameter

These elements do NOT support the `key` parameter and will cause errors if you try to use it:

### Display Elements
- `st.metric()` - Metrics display
- `st.write()` - Text output
- `st.markdown()` - Markdown text
- `st.latex()` - LaTeX formulas
- `st.help()` - Help text

### Status Elements
- `st.info()` - Info messages
- `st.success()` - Success messages
- `st.warning()` - Warning messages
- `st.error()` - Error messages
- `st.exception()` - Exception display

### Chart Elements
- `st.line_chart()` - Line charts
- `st.bar_chart()` - Bar charts
- `st.area_chart()` - Area charts
- `st.scatter_chart()` - Scatter plots
- `st.map()` - Maps
- `st.plotly_chart()` - Plotly charts
- `st.altair_chart()` - Altair charts
- `st.vega_lite_chart()` - Vega-Lite charts
- `st.pydeck_chart()` - PyDeck charts

### Progress Elements
- `st.progress()` - Progress bars
- `st.spinner()` - Loading spinners
- `st.balloons()` - Celebration balloons
- `st.snow()` - Snow animation

## Handling Duplicate Element ID Errors

### For Elements That Support `key`
Use unique keys to prevent duplicate ID errors:

```python
# Good - Using unique keys
for i, item in enumerate(items):
    st.text_input(f"Input {i}", key=f"input_{i}")
    st.button(f"Button {i}", key=f"button_{i}")
    st.dataframe(data, key=f"dataframe_{i}")
```

### For Elements That Don't Support `key`
Use layout containers to separate elements:

```python
# Good - Using columns to separate metrics
col1, col2, col3 = st.columns(3)
col1.metric("Metric 1", "Value 1")
col2.metric("Metric 2", "Value 2")
col3.metric("Metric 3", "Value 3")

# Good - Using containers for other elements
for i, item in enumerate(items):
    with st.container():
        st.info(f"Info {i}")
        st.write(f"Content {i}")
```

## Common Patterns

### Document Processing Example
```python
def display_document_info(documents):
    for doc_name, doc_data in documents.items():
        with st.expander(f"📄 {doc_name}"):
            # Metrics don't support key, use columns
            col1, col2, col3 = st.columns(3)
            col1.metric("File Size", doc_data['size'])
            col2.metric("File Type", doc_data['type'])
            col3.metric("Status", doc_data['status'])
            
            # Dataframes support key
            if 'data' in doc_data:
                st.dataframe(doc_data['data'], key=f"data_{hash(doc_name)}")
            
            # Text areas support key
            if 'content' in doc_data:
                st.text_area("Content", doc_data['content'], 
                           key=f"content_{hash(doc_name)}")
```

### Form Processing Example
```python
def create_form_section():
    with st.form("my_form"):
        # All form elements support key
        name = st.text_input("Name", key="form_name")
        email = st.text_input("Email", key="form_email")
        age = st.number_input("Age", key="form_age")
        
        submitted = st.form_submit_button("Submit", key="form_submit")
        
        if submitted:
            st.success(f"Form submitted: {name}, {email}, {age}")
```

## Best Practices

1. **Always use unique keys** for elements that support them
2. **Use layout containers** (columns, containers, expanders) for elements that don't support keys
3. **Generate keys based on content** (filename, index, counter) rather than static values
4. **Avoid hash collisions** - `hash()` can produce the same value for different strings
5. **Use counters or timestamps** for guaranteed uniqueness
6. **Test with multiple items** to ensure no duplicate ID errors
7. **Use descriptive key names** for better debugging

### Key Generation Strategies

#### ❌ Avoid: Hash-based keys (can collide)
```python
# BAD - hash() can produce same values
unique_key = f"preview_text_{hash(doc_name)}"
```

#### ✅ Good: Counter-based keys
```python
# GOOD - guaranteed unique
self._key_counter += 1
unique_key = f"preview_text_{doc_name}_{self._key_counter}"
```

#### ✅ Good: Timestamp-based keys
```python
# GOOD - timestamp ensures uniqueness
import time
unique_key = f"preview_text_{doc_name}_{int(time.time() * 1000)}"
```

#### ✅ Good: Content-based keys
```python
# GOOD - include content snippet for uniqueness
content_snippet = content[:50].replace(' ', '_')
unique_key = f"preview_text_{doc_name}_{content_snippet}"
```

## Error Resolution

### TypeError: metric() got an unexpected keyword argument 'key'
**Solution**: Remove the `key` parameter from `st.metric()` calls and use columns instead.

### StreamlitDuplicateElementId
**Solution**: Add unique `key` parameters to elements that support them, or use layout containers for elements that don't.

### KeyError: 'key'
**Solution**: Ensure the element supports the `key` parameter before using it.

This guide should help you avoid common Streamlit element ID issues and create robust applications that handle multiple dynamic elements correctly.
