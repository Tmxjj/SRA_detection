
FROM registry.cn-shanghai.aliyuncs.com/qiancen/qiancen:pytorch_2.2.2-cuda12.1-cudnn8-runtime as base
# FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime as base


RUN sed -i 's%http://archive.ubuntu.com/ubuntu%https://mirrors.tuna.tsinghua.edu.cn/ubuntu%' /etc/apt/sources.list && \
    sed -i 's%http://security.ubuntu.com/ubuntu%https://mirrors.tuna.tsinghua.edu.cn/ubuntu%' /etc/apt/sources.list

RUN apt-get update && apt-get install -y vim curl procps net-tools

RUN pip install -U pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn


COPY requirements.txt ./llm-enterprise-requirements.txt
RUN pip3 install -r llm-enterprise-requirements.txt --no-cache-dir

COPY ./ .

ENV ENV=prod
ENV PORT ""

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
ENV TZ="Asia/Shanghai"



WORKDIR /workspace

# 将 PYTHONPATH 设置为包含 /workspace 目录
ENV PYTHONPATH="/workspace:$PYTHONPATH"

CMD [ "bash", "llm_start.sh"]



