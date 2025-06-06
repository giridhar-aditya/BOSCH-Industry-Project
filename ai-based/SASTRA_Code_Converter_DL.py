# -*- coding: utf-8 -*-
"""Test_Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ClhL5ld-yj340Q8qBlw0PyjiwqHK37bn
"""

import torch
import torch.nn as nn
import numpy as np
import re
from model import build_transformer
from config import get_config

from torch.utils.data import Dataset, DataLoader, random_split
from torch.optim.lr_scheduler import LambdaLR
from torch.optim import AdamW
from tqdm import tqdm
import os
from pathlib import Path
import csv

cpp_vocabulary = {
    # C++ Reserved Keywords
    "alignas": 1, "alignof": 2, "and": 3, "and_eq": 4, "asm": 5, "atomic_cancel": 6, "atomic_commit": 7,
    "atomic_noexcept": 8, "auto": 9, "bitand": 10, "bitor": 11, "bool": 12, "break": 13, "case": 14,
    "catch": 15, "char": 16, "char16_t": 17, "char32_t": 18, "char8_t": 19, "class": 20, "compl": 21,
    "concept": 22, "const": 23, "consteval": 24, "constexpr": 25, "constinit": 26, "const_cast": 27,
    "continue": 28, "co_await": 29, "co_return": 30, "co_yield": 31, "decltype": 32, "default": 33,
    "delete": 34, "do": 35, "double": 36, "dynamic_cast": 37, "else": 38, "enum": 39, "explicit": 40,
    "export": 41, "extern": 42, "false": 43, "float": 44, "for": 45, "friend": 46, "goto": 47, "if": 48,
    "inline": 49, "int": 50, "long": 51, "mutable": 52, "namespace": 53, "new": 54, "noexcept": 55,
    "not": 56, "not_eq": 57, "nullptr": 58, "operator": 59, "or": 60, "or_eq": 61, "private": 62,
    "protected": 63, "public": 64, "reflexpr": 65, "register": 66, "reinterpret_cast": 67, "requires": 68,
    "return": 69, "short": 70, "signed": 71, "sizeof": 72, "static": 73, "static_assert": 74,
    "static_cast": 75, "struct": 76, "switch": 77, "synchronized": 78, "template": 79, "this": 80,
    "thread_local": 81, "throw": 82, "true": 83, "try": 84, "typedef": 85, "typeid": 86, "typename": 87,
    "union": 88, "unsigned": 89, "using": 90, "virtual": 91, "void": 92, "volatile": 93, "wchar_t": 94,
    "while": 95, "xor": 96, "xor_eq": 97,

    # Operators
    "!": 98, "!=": 99, "%": 100, "%=": 101, "&": 102, "&&": 103, "&=": 104, "*": 105, "**": 106, "**=": 107,
    "*=": 108, "+": 109, "++": 110, "+=": 111, "-": 112, "--": 113, "-=": 114, "->": 115, "->*": 116,
    "/": 117, "/=": 118, "<": 119, "<<": 120, "<<=": 121, "<=": 122, "=": 123, "==": 124, ">": 125, ">=": 126,
    ">>": 127, ">>=": 128, "?": 129, "^": 130, "^=": 131, "|": 132, "||": 133, "|=": 134, "~": 135,

    # Punctuation
    ",": 136, ".": 137, "...": 138, ":": 139, "::": 140, ";": 141, "[": 142, "]": 143, "{": 144, "}": 145,
    "(": 146, ")": 147,

    # Library Methods
    "bind": 148, "cerr": 149, "cin": 150, "cout": 151, "endl": 152, "future": 153, "getline": 154,
    "lock_guard": 155, "make_shared": 156, "make_unique": 157, "move": 158, "shared_ptr": 159, "swap": 160,
    "thread": 161, "unique_ptr": 162,

    # Preprocessor Directives
    "#define": 163, "#elif": 164, "#else": 165, "#endif": 166, "#ifdef": 167, "#ifndef": 168, "#include": 169,
    "#pragma": 170, "#": 171,

    # Special Tokens
    "[EOS]": 172, "[PAD]": 173, "[SOS]": 174, "<num>": 175, "<str>": 176, "<var>": 177,

    # Libraries
    "algorithm": 178, "chrono": 179, "cmath": 180, "condition_variable": 181, "deque": 182, "fstream": 183,
    "functional": 184, "iomanip": 185, "iostream": 186, "map": 187, "memory": 188, "mutex": 189, "numeric": 190,
    "queue": 191, "set": 192, "string": 193, "thread": 194, "unordered_map": 195, "vector": 196, "main": 197, "include": 198
}

cpp_vocab = {
    # C++ Reserved Keywords
    "alignas": 1, "alignof": 2, " and ": 3, " and_eq ": 4, "asm": 5, "atomic_cancel": 6, "atomic_commit": 7,
    "atomic_noexcept": 8, "auto ": 9, " bitand ": 10, " bitor ": 11, "bool ": 12, "break": 13, "case ": 14,
    "catch": 15, "char ": 16, "char16_t ": 17, "char32_t ": 18, "char8_t ": 19, "class ": 20, "compl ": 21,
    "concept ": 22, "const ": 23, "consteval ": 24, "constexpr ": 25, "constinit ": 26, "const_cast": 27,
    "continue": 28, "co_await ": 29, "co_return ": 30, "co_yield ": 31, "decltype": 32, "default": 33,
    "delete ": 34, "do": 35, "double ": 36, "dynamic_cast": 37, "else": 38, "enum ": 39, "explicit ": 40,
    "export ": 41, "extern ": 42, "false": 43, "float ": 44, "for": 45, "friend ": 46, "goto ": 47, "if": 48,
    "inline ": 49, "int ": 50, "long ": 51, "mutable ": 52, "namespace ": 53, "new ": 54, "noexcept": 55,
    "not ": 56, " not_eq ": 57, "nullptr": 58, " operator": 59, " or ": 60, " or_eq ": 61, "private": 62,
    "protected": 63, "public": 64, "reflexpr": 65, "register ": 66, "reinterpret_cast": 67, "requires ": 68,
    "return ": 69, "short ": 70, "signed ": 71, "sizeof": 72, "static ": 73, "static_assert": 74,
    "static_cast": 75, "struct ": 76, "switch": 77, "synchronized": 78, "template": 79, "this": 80,
    "thread_local ": 81, "throw ": 82, "true": 83, "try": 84, "typedef ": 85, "typeid": 86, "typename ": 87,
    "union ": 88, "unsigned ": 89, "using ": 90, "virtual ": 91, "void ": 92, "volatile ": 93, "wchar_t ": 94,
    "while": 95, " xor ": 96, " xor_eq ": 97,

    # Operators
    "!": 98, "!=": 99, "%": 100, "%=": 101, "&": 102, "&&": 103, "&=": 104, "*": 105, "**": 106, "**=": 107,
    "*=": 108, "+": 109, "++": 110, "+=": 111, "-": 112, "--": 113, "-=": 114, "->": 115, "->*": 116,
    "/": 117, "/=": 118, "<": 119, "<<": 120, "<<=": 121, "<=": 122, "=": 123, "==": 124, ">": 125, ">=": 126,
    ">>": 127, ">>=": 128, "?": 129, "^": 130, "^=": 131, "|": 132, "||": 133, "|=": 134, "~": 135,

    # Punctuation
    ",": 136, ".": 137, "...": 138, ":": 139, "::": 140, ";": 141, "[": 142, "]": 143, "{": 144, "}": 145,
    "(": 146, ")": 147,

    # Library Methods
    "bind": 148, "cerr": 149, "cin": 150, "cout": 151, "endl": 152, "future": 153, "getline": 154,
    "lock_guard": 155, "make_shared": 156, "make_unique": 157, "move": 158, "shared_ptr": 159, "swap": 160,
    "thread": 161, "unique_ptr": 162,

    # Preprocessor Directives
    "#define ": 163, "#elif ": 164, "#else ": 165, "#endif ": 166, "#ifdef ": 167, "#ifndef ": 168, "#include ": 169,
    "#pragma ": 170, "#": 171,

    # Special Tokens
    "[EOS]": 172, "[PAD]": 173, "[SOS]": 174, "<num>": 175, "<str>": 176, "<var>": 177,

    # Libraries
    "algorithm": 178, "chrono": 179, "cmath": 180, "condition_variable": 181, "deque": 182, "fstream": 183,
    "functional": 184, "iomanip": 185, "iostream": 186, "map": 187, "memory": 188, "mutex": 189, "numeric": 190,
    "queue": 191, "set": 192, "string": 193, "thread": 194, "unordered_map": 195, "vector": 196, "main": 197, "include": 198
}



rust_vocabulary = {
    # Rust Reserved Keywords
    'as': 1, 'async': 2, 'await': 3, 'crate': 4, 'fn': 5, 'impl': 6, 'in': 7,
    'let': 8, 'loop': 9, 'match': 10, 'mod': 11, 'move': 12, 'mut': 13, 'pub': 14,
    'ref': 15, 'self': 16, 'Self': 17, 'super': 18, 'trait': 19, 'type': 20,
    'unsafe': 21, 'use': 22, 'where': 23, 'dyn': 24, 'abstract': 25, 'become': 26,
    'box': 27, 'final': 28, 'macro': 29, 'override': 30, 'priv': 31, 'typeof': 32,
    'unsized': 33, 'yield': 34, 'break': 35, 'continue': 36, 'else': 37, 'enum': 38,
    'extern': 39, 'false': 40, 'for': 41, 'if': 42, 'return': 43, 'static': 44,
    'struct': 45, 'true': 46, 'while': 47, 'const': 48, 'do': 49, 'try': 50, 'virtual': 51, 'union': 52,

    # Rust Operators and Punctuation (Overlapping with C++)
    '+': 52, '-': 53, '*': 54, '/': 55, '%': 56, '==': 57, '!=': 58,
    '<': 59, '>': 60, '<=': 61, '>=': 62, '&&': 63, '||': 64, '!': 65,
    '&': 66, '|': 67, '^': 68, '~': 69, '<<': 70, '>>': 71, '=': 72,
    '?': 73, ':': 74, ',': 75, '.': 76, '->': 77, '=>': 78, '::': 79,

    # Additional Tokens for Rust
    '<var>': 80, '<num>': 81, '<str>': 82, ';': 83,
    '[SOS]': 84, '[EOS]': 85, '[PAD]': 86,
    '(': 87, ')': 88, '[': 89, ']': 90, '{': 91, '}': 92,

    # Rust Crates and Modules
    'std': 93, 'io': 94, 'fs': 95, 'thread': 96, 'sync': 97,
    'sync::Mutex': 98, 'sync::Arc': 99, 'env': 100, 'path': 101,
    'time': 102, 'net': 103, 'tokio': 104, 'futures': 105, 'async-std': 106,

    # Built-in Functions (Rust)
    'println': 107, 'format!': 108, 'panic!': 109, 'assert!': 110, 'dbg!': 111,
    'fs::read_to_string': 112, 'fs::write': 113, 'thread::spawn': 114,
    'sync::Arc::new': 115, 'sync::Mutex::new': 116, 'env::var': 117,
    'net::TcpStream': 118, 'net::TcpListener': 119, 'zip':121, 'rev':122,

    # Additional Built-in Functions and Libraries
    'main': 120, 'print!': 121, 'Option': 122, 'Result': 123, 'Some': 124, 'None': 125,
    'Ok': 126, 'Err': 127, 'Vec': 128, 'String': 129, 'Box': 130, 'Clone': 131, 'Copy': 132,
    'Drop': 133, 'PartialEq': 134, 'PartialOrd': 135, 'Iterator': 136, 'HashMap': 137,
    'HashSet': 138, 'Rc': 139, 'Arc': 140, 'RefCell': 141, 'Mutex': 142, 'fs': 143,
    'io': 144, 'env': 145, 'path': 146, 'time': 147, 'thread': 148, 'zip':0, 'rev':0,

    # Special Tokens
    '#': 149, '"': 150, "'": 151, '`': 152, "i8": 1, "i16": 2, "i32": 3, "i64": 4, "i128": 5,
    "isize": 6, "u8": 7, "u16": 8, "u32": 9, "u64": 10, "u128": 11, "usize": 12, "f32": 13, "f64": 14, "new": 15, "step_by": 16,
    "iter": 17, "len": 18, "chars": 19, "stdin": 21, "unwrap":22, "read_line": 23, "trim": 24, "parse": 25,
    "std": 26, "io": 27, "fs": 28, "thread": 29, "sync": 30, "sync::Mutex": 31, "sync::Arc": 32
}

rust_vocabulary_1 = {
    # Rust Reserved Keywords
    'as ': 1, 'async ': 2, 'await ': 3, 'crate': 4, 'fn ': 5, 'impl ': 6, ' in ': 7,
    'let ': 8, 'loop ': 9, 'match ': 10, 'mod': 11, 'move ': 12, 'mut ': 13, 'pub ': 14,
    'ref ': 15, 'self ': 16, 'Self ': 17, 'super ': 18, 'trait ': 19, 'type ': 20,
    'unsafe ': 21, 'use ': 22, 'where ': 23, 'dyn': 24, 'abstract': 25, 'become': 26,
    'box': 27, 'final': 28, 'macro': 29, 'override': 30, 'priv': 31, 'typeof': 32,
    'unsized': 33, 'yield': 34, 'break ': 35, 'continue ': 36, 'else ': 37, 'enum': 38,
    'extern ': 39, 'false ': 40, 'for ': 41, 'if ': 42, 'return ': 43, 'static ': 44,
    'struct ': 45, 'true ': 46, 'while ': 47, 'const ': 48, 'do': 49, 'try': 50, 'virtual': 51, 'union ': 52,

    # Rust Operators and Punctuation (Overlapping with C++)
    '+': 52, '-': 53, '*': 54, '/': 55, '%': 56, '==': 57, '!=': 58,
    '<': 59, '>': 60, '<=': 61, '>=': 62, '&&': 63, '||': 64, '!': 65,
    '&': 66, '|': 67, '^': 68, '~': 69, '<<': 70, '>>': 71, '=': 72,
    '?': 73, ':': 74, ',': 75, '.': 76, '->': 77, '=>': 78, '::': 79,

    # Additional Tokens for Rust
    '<var>': 80, '<num>': 81, '<str>': 82, ';': 84,
    '[SOS]': 85, '[EOS]': 86, '[PAD]': 87,
    '(': 88, ')': 89, '[': 90, ']': 91, '{': 92, '}': 93,

    # Rust Crates and Modules
    'std': 94, 'io': 95, 'fs': 96, 'thread': 97, 'sync': 98,
    'sync::Mutex': 99, 'sync::Arc': 100, 'env': 101, 'path': 102,
    'time': 103, 'net': 104, 'tokio': 105, 'futures': 106, 'async-std': 107,

    # Built-in Functions (Rust)
    'println': 108, 'format!': 109, 'panic!': 110, 'assert!': 111, 'dbg!': 112,
    'fs::read_to_string': 113, 'fs::write': 114, 'thread::spawn': 115,
    'sync::Arc::new': 116, 'sync::Mutex::new': 117, 'env::var': 118,
    'net::TcpStream': 119, 'net::TcpListener': 120, 'zip':121, 'rev':122,

    # Additional Built-in Functions and Libraries
    'main': 121, 'print!': 122, 'Option': 123, 'Result': 124, 'Some': 125, 'None': 126,
    'Ok': 127, 'Err': 128, 'Vec': 129, 'String': 130, 'Box': 131, 'Clone': 132, 'Copy': 133,
    'Drop': 134, 'PartialEq': 135, 'PartialOrd': 136, 'Iterator': 137, 'HashMap': 138,
    'HashSet': 139, 'Rc': 140, 'Arc': 141, 'RefCell': 142, 'Mutex': 143, 'fs': 144,
    'io': 145, 'env': 146, 'path': 147, 'time': 148, 'thread': 149,

    # Special Tokens
    '#': 150, '"': 151, "'": 152, '`': 153,"i8": 1, "u8": 2, "i16": 3, "u16": 4, "i32": 5,
    "u32": 6, "i64": 7, "u64": 8, "i128": 9, "u128": 10, "isize": 11, "usize": 12, "f32": 13, "f64": 14, "new": 15, "step_by": 16,
    "iter": 17, "len": 18, "chars": 19, "stdin": 21, "unwrap":22, "read_line": 23, "trim": 24, "parse": 25,
    "std": 26, "io": 27, "fs": 28, "thread": 29, "sync": 30, "sync::Mutex": 31, "sync::Arc": 32
}

global cpp_size, rust_size
j=0
for i in cpp_vocabulary:
  cpp_vocabulary[i]=j
  j+=1
j=0
for i in rust_vocabulary:
  rust_vocabulary[i]=j
  j+=1
j=0
for i in rust_vocabulary_1:
  rust_vocabulary_1[i]=j
  j+=1
cpp_size=len(cpp_vocabulary)
rust_size=len(rust_vocabulary)
config = get_config()

class CppTokenizer:
    def __init__(self, vocab,config):
        self.vocab = vocab
        self.token_to_id = {token: idx for idx, token in enumerate(vocab)}
        self.id_to_token = {idx: token for token, idx in self.token_to_id.items()}

    def convert_tokens_to_ids(self, code, variables, constants, strings, pred=False):
        # Your token specification remains the same.
        token_specification = [
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
    ('FIRST', r'\+\+|--|<=|>=|==|!=|\+=|-=|\*=|\/=|%=|&=|\|=|\^='),
    ('SECOND', r'&&|\|\||!|<<|>>'),
    ('COMMENT', r'//.*?$|/\*.*?\*/'),
    ('STRING', r'"(?:\\.|[^\\"])*"'),  # Double-quoted strings
    ('CHAR', r"'(?:\\.|[^\\'])'"),     # Single-quoted characters
    ('NUMBER', r'\b\d+(\.\d*)?([eE][+-]?\d+)?\b'),
    ('WORD', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),  # Words (identifiers)
    ('OPERATOR', r'[+\-*/%&|^!=<>]=?|!=|==|\+\+|--|\|\||&&|<<|>>|[?:]'),
    ('PUNCTUATION', r'[()\[\]{};:.,]'),
        ]

        tokens = []
        tokens_preditct=[]
        token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
        for match in re.finditer(token_re, code, re.DOTALL | re.MULTILINE):
            kind = match.lastgroup
            value = match.group(kind)
            if (kind in ['NEWLINE', 'WHITESPACE']):
                continue
            elif (value not in self.vocab) and (kind == 'WORD'):
                tokens.append(self.vocab.get('<var>'))
                variables.append(value)
                tokens_preditct.append(value)
            elif (value not in self.vocab) and (kind == 'NUMBER'):
                tokens.append(self.vocab.get('<num>'))
                constants.append(value)
                tokens_preditct.append(value)
            elif (value not in self.vocab) and (kind in ['STRING', 'CHAR']):
                tokens.append(self.vocab.get('<str>'))
                strings.append(value)
                tokens_preditct.append(value)
            elif (value in self.vocab):
                tokens.append(self.vocab.get(value))
                tokens_preditct.append(value)
        if(pred==True):
          return tokens_preditct
        else:
          return tokens

    def __call__(self, text, padding='max_length', truncation=True, max_length=config['seq_len'], return_tensors=None, variables=[], constants=[], strings=[]):
        token_ids = self.convert_tokens_to_ids(text, variables, constants, strings)
        token_ids.insert(0, self.vocab.get('[SOS]'))
        token_ids.append(self.vocab.get('[EOS]'))

        if truncation and max_length:
            token_ids = token_ids[:max_length]

        if padding == 'max_length' and max_length:
            pad_length = max_length - len(token_ids)
            token_ids += [self.vocab.get('[PAD]')] * pad_length

        if truncation and max_length:
            token_ids = token_ids[:max_length]
        encoder_input=torch.tensor(token_ids)
        if return_tensors == "pt":
            return {
                "input_ids": encoder_input,
                "attention_mask": (encoder_input != self.vocab.get('[PAD]')).unsqueeze(0).unsqueeze(0).int(),
            }

import re
import torch

class RustTokenizer:
    def __init__(self, vocab, config):
        self.vocab = vocab
        self.token_to_id = {token: idx for idx, token in enumerate(vocab)}
        self.id_to_token = {idx: token for token, idx in self.token_to_id.items()}

    def convert_tokens_to_ids(self, code, variables, constants, strings):
        # Updated token specification with expression recognizer at the top
        token_specification = [
            ('FIRST', r'\+\+|--|<=|>=|==|!=|\+=|-=|\*=|\/=|%=|&=|\|=|\^='),  # High priority operators
            ('SECOND', r'&&|\|\||!|<<|>>'),  # Logical operators
            ('COMMENT', r'//.*?$|/\*.*?\*/'),  # Comments
            ('STRING', r'"(?:\\.|[^\\"])*"'),  # Double-quoted strings
            ('CHAR', r"'(?:\\.|[^\\'])'"),     # Single-quoted characters
            ('NUMBER', r'\b\d+(\.\d*)?([eE][+-]?\d+)?\b'),  # Numbers
            ('WORD', r'\b[a-zA-Z_!][a-zA-Z_0-9]*\b'),  # Identifiers (variables)
            ('OPERATOR', r'[+\-*/%&|^!=<>]=?|!=|==|\+\+|--|\|\||&&|<<|>>|[?:]'),  # Operators
            ('PUNCTUATION', r'[()\[\]{};:.,]'),  # Punctuation
            ('WHITESPACE', r'\s+'),  # Whitespace
            ('NEWLINE', r'\n'),  # Newlines
        ]

        tokens = []
        token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

        for match in re.finditer(token_re, code, re.DOTALL | re.MULTILINE):
            kind = match.lastgroup
            value = match.group(kind)
            if kind in ['NEWLINE', 'WHITESPACE']:
                continue  # Skip whitespace and newlines
            elif (value not in self.vocab) and (kind == 'WORD'):
                tokens.append(self.vocab.get('<var>'))
                variables.append(value)
            elif (value not in self.vocab) and (kind == 'NUMBER'):
                tokens.append(self.vocab.get('<num>'))
                constants.append(value)
            elif (value not in self.vocab) and (kind in ['STRING', 'CHAR']):
                tokens.append(self.vocab.get('<str>'))
                strings.append(value)
            elif value in self.vocab:
                tokens.append(self.vocab.get(value))

        return tokens

    def causal_mask(self, size):
        mask = torch.triu(torch.ones((1, size, size)), diagonal=1).type(torch.int)
        return mask == 0

    def __call__(self, text, padding='max_length', truncation=True, max_length=None, return_tensors=None, variables=[], constants=[], strings=[]):
        token_ids = self.convert_tokens_to_ids(text, variables, constants, strings)
        labels = list(token_ids)
        token_dec = list(token_ids)
        token_dec.insert(0, self.vocab.get('[SOS]'))  # SOS token
        labels.append(self.vocab.get('[EOS]'))     # EOS token

        if truncation and max_length:
            token_dec = token_dec[:max_length]
            labels = labels[:max_length]

        if padding == 'max_length' and max_length:
            pad_length = max_length - len(token_dec)
            label_length = max_length - len(token_ids)
            labels += [self.vocab.get('[PAD]')] * label_length
            token_dec += [self.vocab.get('[PAD]')] * pad_length

        if truncation and max_length:
            token_dec = token_dec[:max_length]
            labels = labels[:max_length]

        decoder_input = torch.tensor(token_dec)
        labels = torch.tensor(labels)

        if return_tensors == "pt":
            return {
                "input_ids": decoder_input,
                "attention_mask": (decoder_input != self.vocab.get('[PAD]')).unsqueeze(0).int() & self.causal_mask((decoder_input.size(0))),  # (1, seq_len) & (1, seq_len, seq_len),
                "labels": labels
            }

class CodeDataset(Dataset):
    def __init__(self, cpp_code, rust_code, cpp_tokenizer,rust_tokenizer, max_length):
        self.cpp_code = cpp_code
        self.rust_code = rust_code
        self.cpp_tokenizer = cpp_tokenizer
        self.rust_tokenizer = rust_tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.cpp_code)

    def __getitem__(self, idx):
        cpp_text = self.cpp_code[idx]
        rust_text = self.rust_code[idx]

        inputs = self.cpp_tokenizer(cpp_text, padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')
        targets = self.rust_tokenizer(rust_text, padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')
        return {
            'encoder_input': inputs['input_ids'],
            'encoder_mask': inputs['attention_mask'],
            'labels': targets['labels'],
            'decoder_input':targets['input_ids'],
            'decoder_mask':targets['attention_mask']
        }

cpp_tokenizer = CppTokenizer(cpp_vocabulary,config)
rust_tokenizer = RustTokenizer(rust_vocabulary,config)

def get_model(config):
    model = build_transformer(cpp_size, rust_size, config["seq_len"], config['seq_len'], d_model=config['d_model'])
    return model

def causal_mask(size):
    mask = torch.triu(torch.ones((1, size, size)), diagonal=1).type(torch.int)
    return mask == 0

def Validate(model,cpp_code,validate=True):
    def Convert(decoded, variables, constants, strings):
        if rust_vocabulary_1['for '] in decoded:
                variables.pop(0)
        output_lst = []
        output_lin = ""
        var_index = 0
        const_index = 0
        str_index = 0

        for i in decoded:
            if i == rust_vocabulary["[PAD]"]:
                continue
            elif i == rust_vocabulary["<var>"]:
                if var_index < len(variables):
                    output_lst.append(variables[var_index])
                    output_lin += variables[var_index]
                    var_index += 1
            elif i == rust_vocabulary["<num>"]:
                if const_index < len(constants):
                    output_lst.append(constants[const_index])
                    output_lin += constants[const_index]
                    const_index += 1
            elif i == rust_vocabulary["<str>"]:
                if str_index < len(strings):
                    output_lst.append(strings[str_index])
                    output_lin += strings[str_index]
                    str_index += 1
            else:
                for j in rust_vocabulary_1:
                    if i == rust_vocabulary_1[j]:
                        output_lst.append(j)
                        output_lin += j
                        break

        return output_lin.strip(), output_lst

    def test_model_line_by_line(
        model, cpp_tokenizer, cpp_lines, max_length, variables=[], constants=[], strings=[]
    ):
        cpp_keywords = [
    "alignas", "alignof", "asm", "auto", "bitand", "bitor", "bool", "break",
    "case", "catch", "char", "char8_t", "char16_t", "char32_t", "class",
    "const", "constexpr", "const_cast", "continue", "co_await", "co_return",
    "co_yield", "decltype", "default", "delete", "do", "double", "dynamic_cast",
    "else", "enum", "explicit", "export", "extern", "false", "float", "for",
    "friend", "goto", "if", "import", "inline", "int", "long", "mutable",
    "namespace", "new", "nullptr", "operator", "or", "or_eq", "private",
    "protected", "public", "reinterpret_cast", "requires", "return", "short",
    "signed", "sizeof", "static", "static_assert", "static_cast", "struct",
    "switch", "template", "this", "throw", "true", "try", "typedef", "typeid",
    "typename", "union", "unsigned", "using", "virtual", "void", "volatile",
    "wchar_t", "while", "xor","xor_eq", 'iostream', 'vector', 'string', 'map', 'cmath',
    'algorithm', 'set', 'unordered_map', 'memory', 'functional',
    'queue', 'deque', 'fstream', 'iomanip', 'chrono',
    'thread', 'mutex', 'condition_variable', 'numeric',
    'cin', 'cout', 'cerr', 'endl', 'getline',
    'vector', 'string', 'map', 'set', 'unordered_map',
    'unique_ptr', 'shared_ptr', 'make_shared', 'bind',
    'thread', 'mutex', 'lock_guard', 'async',
    'future', 'make_unique', 'move', 'swap']
        unary_operators = ["++", "--"]

        model.eval()
        rust_lines = []

        for cpp_line in cpp_lines:
            cpp_line.strip()
            variables = []
            constants = []
            strings = []

            # Check for keywords and unary operators
            tokenized_line = cpp_tokenizer.convert_tokens_to_ids(cpp_line,variables,constants,strings,pred=True)
            has_keywords = any(token in cpp_keywords for token in tokenized_line)
            has_unary_operators = any(op in cpp_line for op in unary_operators)

            if not has_keywords and not has_unary_operators:
                rust_lines.append(cpp_line)  # Directly append the same C++ line
                continue

            with torch.no_grad():
                inputs = cpp_tokenizer(
                    cpp_line,
                    padding="max_length",
                    truncation=True,
                    max_length=max_length,
                    return_tensors="pt",
                    variables=variables,
                    constants=constants,
                    strings=strings,
                )
                source = inputs["input_ids"]
                source_mask = inputs["attention_mask"]
                encoder_output = model.encode(source, source_mask)
                decoder_input = torch.empty(1, 1).fill_(rust_vocabulary_1.get('[SOS]')).type_as(source)

                while True:
                    if decoder_input.size(1) == config["seq_len"]:
                        break

                    # Build mask for target
                    decoder_mask = causal_mask(decoder_input.size(1)).type_as(source_mask)

                    # Calculate output
                    out = model.decode(encoder_output, source_mask, decoder_input, decoder_mask)

                    # Get next token
                    prob = model.project(out[:, -1])
                    _, next_word = torch.max(prob, dim=1)
                    decoder_input = torch.cat(
                        [decoder_input, torch.empty(1, 1).type_as(source).fill_(next_word.item())], dim=1
                    )
                    if next_word == rust_vocabulary_1.get('[EOS]'):  # End token
                        break

                output = decoder_input.tolist()[0]
                final_output, _ = Convert(output, variables, constants, strings)
                rust_lines.append((final_output.lstrip().rstrip())[5:-5])

        return rust_lines


    cpp_lines = cpp_code.strip().split('\n')
    rust_lines = test_model_line_by_line(model, cpp_tokenizer, cpp_lines, config["seq_len"])
    if(validate==True):
        print("Line-by-line conversion of C++ to Rust:")
        for cpp_line, rust_line in zip(cpp_lines, rust_lines):
            print(f"C++: {cpp_line}\nRust: {rust_line}\n")
    else:
      rust_program='\n'.join(rust_lines)
      return rust_program




import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # For image handling
import os
import sys
import torch

def resource_path(relative_path):
    """Get absolute path for resources in PyInstaller .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def process_and_convert():
    input_file = "input.cpp"      # Path to input.cpp
    rust_file = "rust.rs"          # Path to rust.rs
    base_dir = os.path.dirname(input_file)

    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            cpp_code = f.read()
            training_pth=resource_path("Training_1_24.pth")
            config = get_config()
            model = get_model(config)
            print("AI Model is Loading...")
            checkpoint = torch.load(training_pth,map_location=torch.device('cpu'))
            model.load_state_dict(checkpoint['model_state_dict'])
            print("AI Model Loaded Successfully")
            print("Conversion has Started")
            rust_code = Validate(model,cpp_code,validate=False)  # Convert C++ to Rust
        with open(rust_file, "w", encoding="utf-8") as f:
            f.write(rust_code)
            
        print("Success", "Rust file created successfully!")
        os.startfile(base_dir)  # Open folder containing Rust file (Windows)
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e}")
process_and_convert()