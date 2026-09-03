FROM python:3.12.14

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 先安装 torch（CUDA 12.6 版本，使用 PyTorch 官方索引）
RUN pip install torch==2.6.0+cu126 --index-url https://download.pytorch.org/whl/cu126

# 安装项目依赖
COPY requirements.txt .
RUN pip install -r requirements.txt



EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]