#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TIFF测试文件生成器（简化版）
使用PIL直接生成多页TIFF文件，包含中文文字
"""

import os
import sys
import random

# 添加site-packages到路径
site_packages = os.path.join(os.path.dirname(__file__), 'UmiOCR-data', 'site-packages')
sys.path.insert(0, site_packages)


# 中文文本库
SAMPLE_TEXTS = [
    "这是一个测试文档，用于验证OCR识别功能。",
    "人工智能技术正在改变我们的生活方式。",
    "机器学习和深度学习是AI的重要组成部分。",
    "Python是一种功能强大的编程语言。",
    "文档处理是办公自动化的重要环节。",
    "光学字符识别技术可以将图片转换为文本。",
    "批量处理可以提高工作效率。",
    "数据分析和挖掘是大数据时代的关键技术。",
    "自然语言处理让计算机能够理解人类语言。",
    "计算机视觉让机器能够看懂世界。",
    "云计算提供了弹性的计算资源。",
    "网络安全保护着我们的数字资产。",
    "区块链技术正在革新金融行业。",
    "物联网连接着万物，实现智能化。",
    "5G技术带来了更快的网络体验。",
    "虚拟现实和增强现实创造沉浸式体验。",
    "边缘计算降低了网络延迟。",
    "微服务架构提高了系统的可扩展性。",
    "容器技术简化了应用的部署。",
    "持续集成和持续交付加速了软件发布。",
]

PARAGRAPHS = [
    "在数字化时代，文档处理技术变得越来越重要。无论是纸质文件的数字化，还是电子文档的归档管理，都需要高效、准确的工具支持。OCR技术作为连接纸质世界和数字世界的桥梁，发挥着不可替代的作用。",
    "随着人工智能技术的快速发展，图像识别和文字提取的准确率不断提升。现代OCR系统不仅能够识别印刷体文字，还能够处理手写字符、表格、公式等复杂场景，为各行各业提供了强大的解决方案。",
    "多页文档的处理是企业日常工作中常见的需求。无论是合同、报告还是技术文档，都需要进行批量处理和归档。高效的文档处理系统能够显著提升工作效率，减少人工操作成本。",
    "A4纸张是国际标准纸张尺寸，广泛应用于各种文档打印和存储。在数字时代，虽然电子文档越来越普及，但A4仍然是一个重要的标准，许多系统都需要处理A4尺寸的文档。",
    "中文作为世界上使用人数最多的语言之一，其OCR识别具有重要的应用价值。中文字符数量众多，结构复杂，对OCR算法提出了更高的要求。优秀的中文OCR系统需要考虑字形、字体、排版等多个因素。",
]


def create_page_with_pil(width, height, page_num):
    """使用PIL创建包含中文的页面"""
    from PIL import Image, ImageDraw, ImageFont
    import random
    
    # 创建白色背景图像
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # 设置边距
    margin = 100
    y_pos = margin + 80
    
    # 尝试加载中文字体
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
        "C:/Windows/Fonts/msyh.ttf",    # 微软雅黑
        "C:/Windows/Fonts/simkai.ttf",  # 楷体
    ]
    
    # 标题字体（Word小二号，约22pt）
    title_font_size = 36
    title_font = None
    for font_path in font_paths:
        try:
            title_font = ImageFont.truetype(font_path, title_font_size)
            break
        except:
            continue
    
    if title_font is None:
        title_font = ImageFont.load_default()
    
    # 正文字体（Word 5号字，约10.5pt）
    text_font_size = 24
    text_font = None
    for font_path in font_paths:
        try:
            text_font = ImageFont.truetype(font_path, text_font_size)
            break
        except:
            continue
    
    if text_font is None:
        text_font = ImageFont.load_default()
    
    # 小字体（Word小5号字）
    small_font_size = 20
    small_font = None
    for font_path in font_paths:
        try:
            small_font = ImageFont.truetype(font_path, small_font_size)
            break
        except:
            continue
    
    if small_font is None:
        small_font = ImageFont.load_default()
    
    # 绘制标题
    title = f"测试文档 - 第 {page_num} 页"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((width / 2 - title_width / 2, margin), title, font=title_font, fill='black')
    
    # 绘制分隔线
    draw.line([margin, margin + 70, width - margin, margin + 70], fill='black', width=3)
    
    # 绘制段落
    paragraph = random.choice(PARAGRAPHS)
    y_pos += 80
    
    # 简单的文本换行处理
    max_width = width - 2 * margin
    line_text = ""
    
    for char in paragraph:
        test_line = line_text + char
        line_bbox = draw.textbbox((0, 0), test_line, font=text_font)
        line_width = line_bbox[2] - line_bbox[0]
        
        if line_width < max_width:
            line_text = test_line
        else:
            draw.text((margin, y_pos), line_text, font=text_font, fill='black')
            y_pos += 35
            line_text = char
    
    if line_text:
        draw.text((margin, y_pos), line_text, font=text_font, fill='black')
        y_pos += 50
    
    # 绘制测试短句标签
    draw.text((margin, y_pos), "测试短句：", font=small_font, fill='black')
    y_pos += 40
    
    # 绘制短句
    for i in range(3):
        sample_text = random.choice(SAMPLE_TEXTS)
        draw.text((margin + 30, y_pos), f"• {sample_text}", font=small_font, fill='black')
        y_pos += 35
    
    # 绘制页码
    page_num_text = f"- {page_num} -"
    page_num_bbox = draw.textbbox((0, 0), page_num_text, font=small_font)
    page_num_width = page_num_bbox[2] - page_num_bbox[0]
    draw.text((width / 2 - page_num_width / 2, height - margin), page_num_text, font=small_font, fill='black')
    
    return img


def generate_multipage_tiff(output_path, num_pages=5, dpi=300):
    """
    生成多页TIFF文件（使用PIL直接渲染中文）
    
    参数:
        output_path: 输出文件路径
        num_pages: 页数
        dpi: 分辨率（DPI）
    """
    # A4尺寸（毫米）-> 像素
    # A4: 210mm x 297mm
    width_mm = 210
    height_mm = 297
    
    # 转换为像素（1英寸=25.4毫米）
    width = int(width_mm * dpi / 25.4)
    height = int(height_mm * dpi / 25.4)
    
    print(f"生成 {num_pages} 页TIFF文件...")
    print(f"尺寸: {width} x {height} 像素 (A4, {dpi} DPI)")
    print(f"输出路径: {output_path}")
    
    # 直接使用PIL创建所有页面
    print("正在创建页面（使用PIL渲染中文）...")
    from PIL import Image
    
    images = []
    for page_num in range(1, num_pages + 1):
        print(f"正在生成第 {page_num}/{num_pages} 页...")
        img = create_page_with_pil(width, height, page_num)
        images.append(img)
    
    # 保存为多页TIFF
    print("正在保存TIFF文件...")
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        format='TIFF',
        compression='tiff_deflate'  # 使用压缩减小文件大小
    )
    
    # 关闭所有图像
    for img in images:
        img.close()
    
    print(f"✓ 成功生成文件: {output_path}")
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / 1024 / 1024
        print(f"✓ 文件大小: {file_size:.2f} MB")
        print(f"✓ 文件格式: 多页TIFF（Windows照片查看器兼容）")
        print(f"✓ 中文支持: 使用PIL渲染中文字体")


def generate_multiple_tiff_files(output_dir, num_files=3, pages_per_file=5):
    """生成多个TIFF文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\n在 {output_dir} 目录下生成 {num_files} 个测试文件...\n")
    
    for i in range(1, num_files + 1):
        filename = f"test_document_{i:02d}.tiff"
        output_path = os.path.join(output_dir, filename)
        generate_multipage_tiff(output_path, num_pages=pages_per_file)
        print()


def main():
    """主函数"""
    print("=" * 60)
    print("TIFF测试文件生成器（简化版）")
    print("=" * 60)
    print()
    
    # 配置参数
    NUM_FILES = 3           # 生成文件数量
    PAGES_PER_FILE = 5      # 每个文件的页数
    DPI = 300               # 分辨率
    OUTPUT_DIR = "./test_tiff_files"  # 输出目录
    
    # 生成文件
    generate_multiple_tiff_files(OUTPUT_DIR, NUM_FILES, PAGES_PER_FILE)
    
    print("=" * 60)
    print("生成完成！")
    print(f"共生成 {NUM_FILES} 个文件，每个文件 {PAGES_PER_FILE} 页")
    print(f"文件保存在: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)
    print("\n提示：您现在可以在Umi-OCR中导入这些TIFF文件进行OCR测试")
    print()


if __name__ == "__main__":
    main()