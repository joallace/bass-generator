# lstm-bass-generator
A bass tab generator using a LSTM approach

## Contents
- [Motivation](#Motivation)
- [Setup](#Setup)
- [Data](#Data)
- [Scripts](#Scripts)

## Motivation

The purpose of this Artificial Intelligence project is to craft bass songs from patterns of different bands and musics

## Setup

- tensorflow
```shell
$ pip install tensorflow
```
- GuitarPro
```shell
$ pip install PyGuitarPro
```

## Data

The data was gathered from the site songsterr, using their plugin to download the songs.

## Scripts
Antes de tudo, gostaria de salientar que ao me referir ao formato **.gpx**, na verdade estou me referindo à família de arquivos Guitar Pro das versões .gp3, .gp4 e .gp5\
A execução dos scripts é feita exclusivamente pelo terminal. Seguem abaixo suas descrições.

### bass_ripper.py

Esse script possibilita fazer a separação, ou *rip*, das tracks de baixo de arquivos .gpx em um certo diretório.

```bash
python bass_ripper.py [diretorio de entrada] [diretorio de saida]
```
**SEMPRE** realize a separação das tracks antes de fazer a conversão dos arquivos.

### converter.py
Esse script, como o nome sugere, será responsável pela conversão dos arquivos, podendo ser feita a conversão de .gpx para .txt e vice-versa. A saída sempre será um arquivo *"output.txt"*

**Conversão para .txt:**

```bash
python converter.py [-t ou --txt] [diretorio de entrada]
```
O arquivo de texto será escrito da seguinte forma:

1. Compasso

```bash
m N D
```
A linha que representa um compasso, ou measure em inglês, sempre iniciará com um **m**, e terá dois parâmetros, sendo eles o numerador **N** e o denominador **D** da assinatura do tempo.

**Obs:** O compasso **SEMPRE** tem que terminar com uma batida de código *b 0 00*


2. Batida

```bash
b D PT
```
A linha que representa uma batida sempre iniciará com um **b**, e terá três parâmetros, sendo eles a duração da batida **D**, a presença do ponto **P** e o tipo da batida **T**.


3. Nota

```bash
n C N THS
```
A linha que representa uma nota sempre iniciará com um **n**, e terá cinco parâmetros, sendo eles a corda do baixo **C**, a nota tocada **N**, o tipo da nota **T**, a presença de Hammer-on **H** e a presença de Slide **S**.


**Conversão para .gpx:**

A leitura sempre será feita pelo arquivo *"output.txt"* gerado pela conversão para .txt
```bash
python converter.py [-g ou --gpx] [arquivo de saida]
```
**Obs:** Opte por gerar arquivos com a extensão **.gp5**.

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**

