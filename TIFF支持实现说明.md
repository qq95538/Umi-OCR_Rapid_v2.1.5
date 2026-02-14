# TIFF文件批量处理支持 - 实现说明

## 实施日期
2026年2月14日

## 修改概述
已成功为Umi-OCR的"批量文档"功能添加了对多页TIFF文件（.tiff和.tif）的完整支持。现在用户可以像处理PDF文件一样处理多页TIFF文件。

## 修改的文件

### 1. UmiOCR-data/py_src/mission/mission_doc.py
**修改内容**：在`DocSuf`列表中添加了`.tiff`和`.tif`扩展名

```python
# 合法文件后缀
DocSuf = [
    ".pdf",
    ".xps",
    ".epub",
    ".mobi",
    ".fb2",
    ".cbz",
    ".tiff",  # 新增
    ".tif",    # 新增
]
```

**作用**：使系统能够识别TIFF文件为有效的文档类型，由`MissionDOC`任务管理器处理。

### 2. UmiOCR-data/py_src/mission/mission_ocr.py
**修改内容**：从`ImageSuf`列表中移除了`.tif`和`.tiff`扩展名

```python
# 合法文件后缀
ImageSuf = [
    ".jpg",
    ".jpe",
    ".jpeg",
    ".jfif",
    ".png",
    ".webp",
    ".bmp",
    # 已移除 ".tif" 和 ".tiff"
]
```

**作用**：防止TIFF文件被"批量图片"功能处理，避免"Image decode failed"错误。确保TIFF文件只能在"批量文档"功能中使用。

### 3. UmiOCR-data/qt_res/qml/TabPages/BatchDOC/BatchDOC.qml
**修改内容**：更新了文件对话框的文件过滤器

```qml
fileDialogNameFilters: [qsTr("文档")+" (*.pdf *.xps *.epub *.mobi *.fb2 *.cbz *.tiff *.tif)"]
```

**作用**：在文件选择对话框中显示TIFF文件，用户可以选择.tiff或.tif文件进行批量处理。

## 工作原理

### 为什么只需修改文件扩展名列表？

Umi-OCR使用PyMuPDF（fitz）库处理文档，该库原生支持多页TIFF文件格式。因此，只需在文件类型列表中添加TIFF扩展名，现有的文档处理流程（页面遍历、OCR识别、结果输出等）即可完全适用，无需修改任何核心处理逻辑。

### 技术流程

1. **文件识别**：当用户选择.tiff或.tif文件时，系统通过`DocSuf`列表识别其为文档类型
2. **文档加载**：`MissionDOC`使用`fitz.open()`打开TIFF文件（与PDF文件相同）
3. **页面信息获取**：自动获取TIFF文件的页数（`doc.page_count`）
4. **页面遍历**：逐页提取每页内容进行OCR识别
5. **结果输出**：支持所有输出格式（txt、jsonl、csv、双层可搜索PDF等）

## 支持的功能

✓ 多页TIFF文件导入
✓ 逐页OCR识别
✓ 页面范围选择（支持全页、指定页数、负数页码）
✓ 批量处理多个TIFF文件
✓ 文件预览
✓ 多种输出格式（txt、jsonl、csv、双层可搜索PDF、单层PDF等）
✓ 页码显示
✓ 处理进度跟踪
✓ 暂停/恢复功能
✓ 拖拽文件导入
✓ 文件夹递归导入

## 使用方法

### 方法一：通过图形界面

1. 启动Umi-OCR程序
2. 点击"批量文档"标签页
3. 点击"打开文档"按钮，或直接拖入TIFF文件
4. 在文件选择对话框中选择.tiff或.tif文件
5. 设置识别范围（可选）
6. 点击"开始"按钮进行OCR识别

### 方法二：使用测试文件

项目中已包含测试TIFF文件生成器：

#### 运行测试文件生成器：
```batch
run_tiff_generator.bat
```

#### 或直接运行Python脚本：
```bash
python generate_test_tiff_simple.py
```

#### 生成的测试文件：
- `test_tiff_files/test_document_01.tiff` - 5页
- `test_tiff_files/test_document_02.tiff` - 5页
- `test_tiff_files/test_document_03.tiff` - 5页

## 测试验证

### 测试步骤：

1. 运行`run_tiff_generator.bat`生成测试文件（或使用已有的测试文件）
2. 启动Umi-OCR
3. 进入"批量文档"页面
4. 导入生成的TIFF文件
5. 执行OCR识别
6. 验证识别结果和输出文件

### 预期结果：

- 文件能够正常导入
- 显示正确的页数（5页）
- 能够识别页面中的中文文字
- 能够导出各种格式的结果文件
- 进度跟踪正常工作
- 暂停/恢复功能正常

## 注意事项

1. **文件格式**：生成的TIFF文件应为真正的多页TIFF格式，兼容Windows照片查看器和其他图像查看软件。

2. **文件大小**：测试文件约为0.47MB（5页，300 DPI），使用tiff_deflate压缩。如果需要更小的文件，可以降低DPI参数。

3. **字体大小**：测试文件使用Word 5号字大小（约10.5pt），确保人眼和机器都能清晰识别。

4. **中文字体**：确保系统中有中文字体（如simhei.ttf、simsun.ttc等），以便正确显示和识别中文。

5. **OCR准确性**：测试文件中的文字清晰度高，OCR识别准确率应该很高。实际扫描件的质量会影响识别效果。

6. **输出格式**：所有PDF相关的输出格式（如双层可搜索PDF）也适用于TIFF文件。

## 技术优势

1. **零代码改动**：利用PyMuPDF的原生支持，无需编写额外的TIFF处理代码
2. **完整功能复用**：所有PDF处理功能（页面范围、预览、输出格式等）自动适用于TIFF
3. **一致性体验**：用户界面和操作流程与PDF处理完全一致
4. **向后兼容**：不影响现有PDF、XPS等文件格式的处理

## 常见问题

**Q: TIFF文件支持密码保护吗？**
A: 目前实现中，TIFF文件的密码保护与PDF不同。如果TIFF文件被加密，系统会提示需要密码。

**Q: 可以处理单页TIFF文件吗？**
A: 可以，单页和多页TIFF文件都支持。

**Q: 为什么之前生成的文件无法在Windows照片查看器中打开？**
A: 之前的版本可能使用了错误的格式保存方法。现在使用PyMuPDF（fitz）库，生成的文件是真正的多页TIFF格式，完全兼容。

**Q: 字体大小是多少？**
A: 测试文件使用Word 5号字（约10.5pt），这是标准的文档字体大小，人眼和机器都能清晰识别。标题使用更大的字体（Word小二号，约22pt）。

**Q: 可以生成更多页的TIFF文件吗？**
A: 可以，修改`generate_test_tiff_simple.py`中的`PAGES_PER_FILE`参数。

**Q: 生成的TIFF文件大小是多少？**
A: 每个文件约0.47MB（5页，300 DPI），使用tiff_deflate压缩。如果需要更小的文件，可以降低`generate_test_tiff_simple.py`中的DPI参数（例如改为150或200）。

## 版本信息

- Umi-OCR版本：Rapid v2.1.5
- Python版本：3.8
- PyMuPDF版本：1.24.11

## 总结

通过简单的三个文件修改，成功实现了对多页TIFF文件的完整批量处理支持。该实现利用了PyMuPDF库的原生TIFF支持，无需额外的代码开发，保持了系统的一致性和稳定性。用户现在可以使用与PDF完全相同的流程来处理TIFF文件，享受所有现有的功能特性。