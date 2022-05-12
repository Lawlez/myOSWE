from ubuntu:20.04

RUN useradd -m nftdrm

WORKDIR /home/nftdrm

RUN mkdir /home/nftdrm/lib && \
    mkdir /home/nftdrm/bios

COPY ./remote /home/nftdrm
COPY start.sh /start.sh

RUN chown -R root:nftdrm /home/nftdrm && \
    chmod +x /home/nftdrm/run.sh && \
    chmod +x /home/nftdrm/qemu-system-x86_64 && \
    chown root:nftdrm /start.sh && \
    chmod +x /start.sh

USER nftdrm
EXPOSE 1337
CMD ["/start.sh"]
