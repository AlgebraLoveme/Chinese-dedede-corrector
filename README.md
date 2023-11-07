# 的地得Corrector

# Introduction

的地得 are Chinese words that are super common (just like "be" in English). However, although they have strict usages which are illustrated in the primary school textbook, recently there are many mistakes in novels, movies and TV series. Therefore, this tool is designed to automatically correct the mistakes by enforcing the language rules.

--- Chinese version below ---

``的地得``很常用，并且在小学教科书里面就有详细的用法规定。然而，在没有经过仔细编辑的网络小说和电视剧字幕中，经常会出现``的地得``用法错误。因此，这个工具将自动化修正错误``的``用法。

# Setup

```
conda create -n parse python=3.7
conda activate parse
python -m pip install -r requirements.txt
```

# Clarification
This code applies pkuseg to annotate the sentences and use rule-based conditions to filter and correct improper usage of "的". Since pkuseg makes mistakes, it is possible that this tool mistakenly replaces correct "的" by "地" or "得". Nevertheless, this tool makes conservative corrections in most cases, i.e., the main focus is precision instead of recall. To check the replacement quality, verbose mode prints all replacements in detail.

However, this tool relies on manually designed rules, thus requires further support for the community to make more fine-grained rules.

--- Chinese version below ---

此工具的原理是使用词性标注工具来逐句标定``的''的前后词词性，并以此为基础判定用法是否错误及修复。默认的标注引擎为pkuseg，但也支持使用jieba引擎。由于词性标注引擎并不能做到没有错误，因此有时此工具也会做出错误的判断。尽管如此，此工具使用了更保守的修复策略，尽可能降低错报概率；也正因为如此，有一定可能无法识别到错误用法。

由于经过观察，``的``最常用且绝大多数错误都为误将``地得``写为``的``，因此本工具只检测``的``是否为误用。

# Usage

```bash
python main.py --filename FILE_TO_PROCESS --verbose
```

```
usage: main.py [-h] --filename FILENAME [--savename SAVENAME]
               [--encoding ENCODING] [--parser_engine {pkuseg,jieba}]
               [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME   File to process.
  --savename SAVENAME   File to save.
  --encoding ENCODING   Encoding of the file.
  --parser_engine {pkuseg,jieba}
                        Parser to use.
  --verbose             Verbose mode.
```

## Example

```test.txt``` contains the first ten chapters of the online novel 《全球高武》 by 老鹰吃小鸡. To correct this test file, run
```
python main.py --filename test.txt --verbose
```
A new file ```test.txt.corrected``` will be generated with ``的`` corrected.