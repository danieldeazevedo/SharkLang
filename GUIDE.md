# 🦈 Guia de Instalação do Shark

Este guia mostra como instalar o Shark para usar como comando `shark` no terminal.

---

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Sistema operacional: Windows, Linux ou macOS

---

## 🔧 Instalação

### Passo 1: Organizar os Arquivos

Crie uma pasta para o Shark e organize os arquivos:

```
shark/
├── shark.py           # Interpretador principal
├── shark_cli.py       # CLI tool
└── index.shark        # Seu código (opcional)
```

### Passo 2: Instalação no Sistema

Escolha o método de acordo com seu sistema operacional:

---

## 🐧 Linux / macOS

### Método 1: Usando Symlink (Recomendado)

1. **Torne o CLI executável:**
```bash
chmod +x shark_cli.py
```

2. **Adicione o shebang no topo do `shark_cli.py`** (já incluído):
```python
#!/usr/bin/env python3
```

3. **Crie um symlink no PATH:**
```bash
sudo ln -s /caminho/completo/para/shark_cli.py /usr/local/bin/shark
```

4. **Teste:**
```bash
shark version
shark help
```

### Método 2: Adicionar ao PATH

1. **Adicione a pasta do Shark ao PATH** editando `~/.bashrc` ou `~/.zshrc`:

```bash
export PATH="$PATH:/caminho/completo/para/pasta/shark"
```

2. **Renomeie o arquivo:**
```bash
mv shark_cli.py shark
chmod +x shark
```

3. **Recarregue o shell:**
```bash
source ~/.bashrc  # ou source ~/.zshrc
```

4. **Teste:**
```bash
shark version
```

---

## 🪟 Windows

### Método 1: Usando Batch File

1. **Crie um arquivo `shark.bat`** na mesma pasta:

```batch
@echo off
python "%~dp0shark_cli.py" %*
```

2. **Adicione a pasta ao PATH do Windows:**
   - Abra "Variáveis de Ambiente"
   - Edite a variável `PATH`
   - Adicione o caminho completo da pasta do Shark
   - Clique OK

3. **Teste no CMD ou PowerShell:**
```cmd
shark version
shark help
```

### Método 2: Usando PowerShell Script

1. **Crie um arquivo `shark.ps1`:**

```powershell
python "$PSScriptRoot\shark_cli.py" $args
```

2. **Adicione ao PATH** (mesmo processo acima)

3. **Habilite execução de scripts** (como admin):
```powershell
Set-ExecutionPolicy RemoteSigned
```

4. **Teste:**
```powershell
shark version
```

---

## ✅ Verificar Instalação

Após instalar, teste os comandos:

```bash
# Verificar versão
shark version

# Ver ajuda
shark help

# Executar arquivo
shark init programa.shark

# Executar index.shark automaticamente
shark
```

---

## 🚀 Uso do CLI

### Comandos Disponíveis

```bash
# Executar um arquivo Shark
shark init index.shark
shark run programa.shark

# Executar index.shark automaticamente (se existir no diretório atual)
shark

# REPL interativo
shark repl

# Ajuda
shark help

# Versão
shark version
```

---

## 📝 Exemplos de Uso

### Exemplo 1: Executar Programa

Crie um arquivo `hello.shark`:
```shark
print("Hello, Shark! 🦈");
var x = 10 + 20;
print("Resultado:", x);
```

Execute:
```bash
shark init hello.shark
```

### Exemplo 2: Projeto com index.shark

Estrutura do projeto:
```
meu-projeto/
└── index.shark
```

Conteúdo de `index.shark`:
```shark
var dados = [10, 20, 30, 40, 50];
var μ = mean(dados);
print("Média:", μ);
```

Execute (dentro da pasta):
```bash
shark
```

### Exemplo 3: REPL Interativo

```bash
$ shark repl
🦈 Shark REPL v1.0.0
Type 'exit' to quit

>>> var x = 10;
>>> var y = 20;
>>> print(x + y);
30
>>> exit
Goodbye! 🦈
```

---

## 🔧 Solução de Problemas

### Erro: "Command not found" ou "shark não é reconhecido"

**Linux/macOS:**
- Verifique se o arquivo tem permissão de execução: `chmod +x shark_cli.py`
- Verifique se o PATH está correto: `echo $PATH`
- Use caminho absoluto: `/usr/local/bin/shark`

**Windows:**
- Verifique se a pasta está no PATH do Windows
- Reinicie o terminal após adicionar ao PATH
- Use `shark.bat` em vez de `shark` se necessário

### Erro: "ModuleNotFoundError: No module named 'shark'"

O arquivo `shark_cli.py` precisa importar `shark.py`. Certifique-se de que ambos estão na mesma pasta ou ajuste o import:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from shark import run_shark_file, run_shark
```

### Erro: "Permission denied"

**Linux/macOS:**
```bash
chmod +x shark_cli.py
```

---

## 📦 Instalação Alternativa: Setup.py

Para uma instalação mais profissional, crie um `setup.py`:

```python
from setuptools import setup

setup(
    name='shark-lang',
    version='1.0.0',
    py_modules=['shark', 'shark_cli'],
    entry_points={
        'console_scripts': [
            'shark=shark_cli:main',
        ],
    },
    install_requires=[],
    python_requires='>=3.7',
    author='Your Name',
    description='Shark Programming Language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
```

Instale com:
```bash
pip install -e .
```

Agora `shark` estará disponível globalmente!

---

## 🎯 Próximos Passos

Após instalar, você pode:

1. ✅ Criar seus programas `.shark`
2. ✅ Usar `shark init arquivo.shark` para executar
3. ✅ Experimentar o REPL: `shark repl`
4. ✅ Ler a documentação completa

---

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se Python 3.7+ está instalado: `python --version`
2. Verifique se os arquivos estão na mesma pasta
3. Certifique-se de que tem permissões adequadas
4. Teste executando diretamente: `python shark_cli.py help`

---

## 📚 Estrutura Final Recomendada

```
/usr/local/shark/          # ou C:\Program Files\Shark no Windows
├── shark.py               # Interpretador
├── shark_cli.py           # CLI (ou shark.bat no Windows)
├── README.md              # Documentação
└── examples/              # Exemplos
    ├── hello.shark
    ├── statistics.shark
    └── functions.shark
```

**Symlink/PATH apontando para:**
- Linux/macOS: `/usr/local/bin/shark` → `/usr/local/shark/shark_cli.py`
- Windows: `C:\Program Files\Shark` no PATH do sistema

---

🎉 **Pronto! Agora você pode usar `shark init index.shark` em qualquer lugar!**