# TIFF文件支持 - 功能说明

## 一、功能概述

已成功为Umi-OCR添加了对多页TIFF文件（.tiff和.tif）的支持。现在用户可以像处理PDF文件一样处理多页TIFF文件，包括逐页OCR识别、页面范围选择、批量处理等功能。

## 二、修改的文件

### 1. UmiOCR-data/py_src/mission/mission_doc.py
- 在`DocSuf`列表中添加了`.tiff`和`.tif`扩展名
- 使系统能够识别TIFF文件为有效文档类型

### 2. UmiOCR-data/py_src/mission/mission_ocr.py
- 从`ImageSuf`列表中移除了`.tiff`和`.tif`扩展名
- **重要**：确保TIFF文件不会被当作普通图片处理
- 避免TIFF文件在"批量图片"功能中出现"Image decode failed"错误

### 3. UmiOCR-data/qt_res/qml/TabPages/BatchDOC/BatchDOC.qml
- 更新了文件对话框的文件过滤器
- 添加了`*.tiff`和`*.tif`到支持的文件格式列表

### 4. UmiOCR-data/qt_res/qml/TabPages/PagesManager.qml
- 更新了批量文档页面的帮助文本
- 在支持的格式中添加了`tiff, tif`

## 三、使用方法

### 方法一：使用图形界面
1. 启动Umi-OCR程序
2. 点击"批量文档"标签页
3. 点击"打开文档"按钮，或直接拖入TIFF文件
4. 在文件选择对话框中选择.tiff或.tif文件
5. 设置识别范围（可选）
6. 点击"开始"按钮进行OCR识别

### 方法二：使用测试文件
项目包含了TIFF测试文件生成器，可以生成测试用TIFF文件：

#### 运行测试文件生成器：
```batch
run_tiff_generator.bat
```

#### 或直接运行Python脚本：
```bash
python generate_test_tiff_simple.py
```

#### 生成器功能：
- 自动生成3个测试TIFF文件
- 每个文件包含5页A4幅面内容
- 每页包含随机中文文字和段落
- 分辨率：300 DPI（高质量）
- 文件保存在：`./test_tiff_files/`目录

#### 自定义参数：
编辑`generate_test_tiff_simple.py`中的以下参数：
```python
NUM_FILES = 3           # 生成文件数量
PAGES_PER_FILE = 5      # 每个文件的页数
DPI = 300               # 分辨率
OUTPUT_DIR = "./test_tiff_files"  # 输出目录
```

## 四、技术说明

### 为什么TIFF文件能够直接支持？
Umi-OCR使用PyMuPDF（fitz）库处理文档，该库原生支持多页TIFF文件格式。因此，只需在文件类型列表中添加TIFF扩展名，现有的文档处理流程（页面遍历、OCR识别、结果输出等）即可完全适用。

### 支持的功能：
✓ 多页TIFF文件导入
✓ 逐页OCR识别
✓ 页面范围选择
✓ 批量处理多个TIFF文件
✓ 文件预览
✓ 多种输出格式（txt、jsonl、csv、双层可搜索PDF等）
✓ 页码显示
✓ 处理进度跟踪
✓ 暂停/恢复功能

### TIFF文件特性：
- 支持8位、24位彩色图像
- 支持多种压缩方式
- 支持多页文档
- 标准A4幅面（210mm × 297mm）
- 300 DPI高分辨率，适合OCR识别

## 五、测试验证

### 生成的测试文件：
- `test_document_01.tiff` - 5页 (约0.47 MB)
- `test_document_02.tiff` - 5页 (约0.46 MB)
- `test_document_03.tiff` - 5页 (约0.47 MB)

**文件特性**：
- ✓ 真正的多页TIFF格式（Windows照片查看器兼容）
- ✓ Word 5号字大小（约10.5pt），清晰易读
- ✓ A4幅面，300 DPI高分辨率
- ✓ 每页包含随机中文段落和短句
- ✓ 使用PIL直接渲染中文字体，确保中文正确显示
- ✓ 适合OCR识别测试
- ✓ 文件压缩优化，大小适中

### 测试步骤：
1. 运行`run_tiff_generator.bat`生成测试文件
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

## 六、注意事项

1. **文件大小**：生成的TIFF文件约为0.47MB（每个文件5页），使用300 DPI高分辨率和tiff_deflate压缩。如果需要更小的文件，可以降低DPI参数（例如改为150或200）。

2. **字体大小**：测试文件使用Word 5号字大小（约10.5pt），确保人眼和机器都能清晰识别。标题使用更大的字体（Word小二号，约22pt）以突出显示。

3. **文件格式**：生成的文件是真正的多页TIFF格式，完全兼容Windows照片查看器和其他图像查看软件。

4. **中文字体**：生成器使用PIL直接渲染中文字体，优先使用Windows系统字体（黑体、宋体、微软雅黑等）。如果系统没有这些字体，会回退到默认字体。

5. **中文显示**：当前版本使用PIL渲染中文，确保所有中文字符都能正确显示和识别。

6. **OCR准确性**：测试文件中的文字清晰度高，OCR识别准确率应该很高。实际扫描件的质量会影响识别效果。

7. **输出格式**：所有PDF相关的输出格式（如双层可搜索PDF）也适用于TIFF文件。

## 七、文件清单

### 修改的核心文件：
- `UmiOCR-data/py_src/mission/mission_doc.py` - 添加TIFF到DocSuf（批量文档支持）
- `UmiOCR-data/py_src/mission/mission_ocr.py` - 从ImageSuf移除TIFF（避免批量图片冲突）
- `UmiOCR-data/qt_res/qml/TabPages/BatchDOC/BatchDOC.qml` - 更新文件过滤器
- `UmiOCR-data/qt_res/qml/TabPages/PagesManager.qml` - 更新帮助文本

### 测试工具：
- `generate_test_tiff.py` - 原始版本（需要PIL库）
- `generate_test_tiff_simple.py` - 简化版本（使用fitz库）
- `run_tiff_generator.bat` - Windows批处理启动脚本

### 生成的测试文件：
- `test_tiff_files/test_document_01.tiff`
- `test_tiff_files/test_document_02.tiff`
- `test_tiff_files/test_document_03.tiff`

## 八、常见问题

**Q: 生成的TIFF文件大小是多少？**
A: 每个文件约0.47MB（5页，300 DPI），使用tiff_deflate压缩。如果需要更小的文件，可以降低`generate_test_tiff_simple.py`中的DPI参数（例如改为150或200）。

**Q: 可以生成更多页的TIFF文件吗？**
A: 可以，修改`generate_test_tiff_simple.py`中的`PAGES_PER_FILE`参数。

**Q: TIFF文件支持密码保护吗？**
A: 目前实现中，TIFF文件的密码保护与PDF不同。如果TIFF文件被加密，系统会提示需要密码。

**Q: 可以处理单页TIFF文件吗？**
A: 可以，单页和多页TIFF文件都支持。

**Q: 生成的测试文件文字是乱码怎么办？**
A: 检查系统中是否有中文字体（如simhei.ttf、simsun.ttc等），或修改代码中的字体路径。

**Q: 为什么之前生成的文件无法在Windows照片查看器中打开？**
A: 之前的版本使用了错误的格式保存方法。现在已修复，生成的是真正的多页TIFF格式，完全兼容Windows照片查看器。

**Q: 字体大小是多少？**
A: 测试文件使用Word 5号字（约10.5pt），这是标准的文档字体大小，人眼和机器都能清晰识别。标题使用更大的字体（Word小二号，约22pt）。

## 九、联系与反馈

如有问题或建议，请通过以下方式反馈：
- GitHub Issues
- 项目文档
- 开发者邮箱

---

**版本信息**
- 添加日期：2026年2月14日
- Umi-OCR版本：Rapid v2.1.5
- Python版本：3.8
- PyMuPDF版本：1.24.11