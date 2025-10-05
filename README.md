# 🦈 Shark Language

**Shark** é uma linguagem de programação interpretada, moderna e focada em **matemática e estatística**. Projetada para ser simples, elegante e eficiente, Shark oferece sintaxe limpa com suporte nativo a operações estatísticas e vetorizadas.

## 🌟 Características

- ✅ **Sintaxe limpa e moderna** com declarações explícitas
- ✅ **Operações vetorizadas** automáticas em arrays
- ✅ **Funções estatísticas built-in** (média, desvio padrão, mediana, etc.)
- ✅ **Suporte a símbolos matemáticos** (μ, σ, Σ)
- ✅ **Tipagem opcional** para maior clareza
- ✅ **Funções de primeira classe** com sintaxe `=>`
- ✅ **Ranges naturais** (`1..10`)
- ✅ **Condicionais intuitivos** com `?` e `otherwise`

---

## 📦 Instalação

1. **Baixe o interpretador**: Salve o código Python como `shark.py`
2. **Requisitos**: Python 3.7+ (usa apenas biblioteca padrão)
3. **Pronto para usar!**

```bash
python shark.py               # Executa index.shark se existir
python shark.py programa.shark  # Executa arquivo específico
```

---

## 🚀 Começando

### Hello World

Crie um arquivo `hello.shark`:

```shark
print("Hello, Shark! 🦈");
```

Execute:
```bash
python shark.py hello.shark
```

---

## 📖 Sintaxe Básica

### Variáveis

```shark
// Declaração com tipo explícito
var x: int = 10;
var y: float = 3.14;
var nome: string = "Shark";
var ativo: bool = true;

// Inferência automática de tipo
var z = 20;           // int
var pi = 3.14159;     // float
var msg = "Olá";      // string
```

**Tipos disponíveis:**
- `int` - Números inteiros
- `float` - Números decimais
- `string` - Texto
- `bool` - Booleano (true/false)
- `array` - Arrays/listas

### Operadores

#### Aritméticos
```shark
var soma = 10 + 5;        // 15
var subtracao = 10 - 5;   // 5
var multiplicacao = 10 * 5; // 50
var divisao = 10 / 5;     // 2
var modulo = 10 % 3;      // 1
var potencia = 2 ** 3;    // 8
```

#### Comparação
```shark
x == y   // Igual
x != y   // Diferente
x < y    // Menor que
x > y    // Maior que
x <= y   // Menor ou igual
x >= y   // Maior ou igual
```

#### Lógicos
```shark
x and y  // E lógico
x or y   // OU lógico
not x    // NÃO lógico
```

---

## 🔧 Funções

### Sintaxe Básica com `=>`

```shark
// Função de uma linha
dobro(x) => x * 2;

// Função com tipos explícitos
soma(a: int, b: int): int => a + b;

// Chamando funções
var resultado = dobro(5);
print(resultado);  // 10
```

### Funções com Bloco

```shark
fatorial(n) => {
    ? n <= 1 {
        return 1;
    }
    return n * fatorial(n - 1);
}

var fat = fatorial(5);
print(fat);  // 120
```

### Funções Recursivas

```shark
fibonacci(n) => {
    ? n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

print(fibonacci(10));  // 55
```

---

## 🎯 Condicionais

### Sintaxe com `?` e `otherwise`

```shark
var idade = 18;

? idade >= 18 {
    print("Maior de idade");
} otherwise {
    print("Menor de idade");
}
```

### Condicionais Aninhados

```shark
var nota = 8.5;

? nota >= 9.0 {
    print("Excelente!");
} otherwise {
    ? nota >= 7.0 {
        print("Bom!");
    } otherwise {
        print("Precisa melhorar");
    }
}
```

---

## 🔁 Loops

### Loop `for` com Range

```shark
// Range de 1 a 10 (exclusivo)
for i in 1..11 {
    print(i);
}

// Iterando sobre array
var nums = [1, 2, 3, 4, 5];
for n in nums {
    print(n);
}
```

### Loop `while`

```shark
var contador = 0;

while contador < 5 {
    print("Contador:", contador);
    contador = contador + 1;
}
```

---

## 📊 Arrays

### Criação e Manipulação

```shark
// Criar array
var numeros = [1, 2, 3, 4, 5];

// Operações básicas
print(len(numeros));    // 5
print(sum(numeros));    // 15
print(min(numeros));    // 1
print(max(numeros));    // 5
```

### Operações Vetorizadas

Uma das features mais poderosas do Shark! 🚀

```shark
var vetor = [1, 2, 3, 4, 5];

// Multiplicar todos elementos por 2
var dobro = vetor * 2;
print(dobro);  // [2, 4, 6, 8, 10]

// Elevar ao quadrado
var quadrado = vetor ** 2;
print(quadrado);  // [1, 4, 9, 16, 25]

// Somar dois vetores
var v1 = [1, 2, 3];
var v2 = [4, 5, 6];
var soma = v1 + v2;
print(soma);  // [5, 7, 9]
```

---

## 📈 Funções Estatísticas

Shark possui funções estatísticas nativas!

### Funções Built-in

```shark
var dados = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];

// Medidas de tendência central
var media = mean(dados);
var mediana = median(dados);

// Medidas de dispersão
var desvio = stdev(dados);
var variancia = variance(dados);

// Outras funções
var soma_total = sum(dados);
var minimo = min(dados);
var maximo = max(dados);

print("Média:", media);           // 55.0
print("Mediana:", mediana);       // 55.0
print("Desvio Padrão:", desvio);  // ~30.28
```

### Símbolos Matemáticos

Shark suporta símbolos gregos! ✨

```shark
var dados = [12, 15, 18, 20, 22];

var μ = mean(dados);     // Média (mu)
var σ = stdev(dados);    // Desvio padrão (sigma)
var Σ = sum(dados);      // Soma (sigma maiúsculo)

print("μ:", μ);
print("σ:", σ);
print("Σ:", Σ);
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Análise de Notas

```shark
// Análise de desempenho de alunos
var notas = [7.5, 8.0, 6.5, 9.0, 7.0, 8.5, 9.5, 6.0];

var μ = mean(notas);
var σ = stdev(notas);
var mediana = median(notas);

print("=== Análise de Notas ===");
print("Média:", μ);
print("Desvio Padrão:", σ);
print("Mediana:", mediana);
print("Nota Mínima:", min(notas));
print("Nota Máxima:", max(notas));

? μ >= 7.0 {
    print("✅ Turma aprovada!");
} otherwise {
    print("❌ Turma precisa melhorar");
}
```

### Exemplo 2: Cálculo de Z-Score

```shark
// Normalização de dados (z-score)
normalizar(x, media, desvio) => (x - media) / desvio;

var dados = [10, 15, 20, 25, 30];
var μ = mean(dados);
var σ = stdev(dados);

print("Dados normalizados (z-score):");
for valor in dados {
    var z = normalizar(valor, μ, σ);
    print(valor, "=> z =", z);
}
```

### Exemplo 3: Simulação Monte Carlo

```shark
// Calcular média de múltiplas amostras
calcular_estatisticas(amostras) => {
    var medias = [];

    for amostra in amostras {
        var m = mean(amostra);
        medias = medias;  // Acumular resultados
    }

    return mean(medias);
}

var amostra1 = [10, 20, 30];
var amostra2 = [15, 25, 35];
var amostra3 = [12, 22, 32];

print("Média das médias:", 
      mean([mean(amostra1), mean(amostra2), mean(amostra3)]));
```

### Exemplo 4: Regressão Linear Simples

```shark
// Calcular coeficiente angular (slope)
regressao(x, y) => {
    var n = len(x);
    var μx = mean(x);
    var μy = mean(y);

    // Cálculo da inclinação
    var xy = x * y;
    var x2 = x ** 2;

    var numerador = sum(xy) - n * μx * μy;
    var denominador = sum(x2) - n * μx * μx;

    return numerador / denominador;
}

var x_valores = [1, 2, 3, 4, 5];
var y_valores = [2, 4, 6, 8, 10];

var slope = regressao(x_valores, y_valores);
print("Inclinação da reta:", slope);  // 2.0
```

### Exemplo 5: Detecção de Outliers

```shark
// Detectar outliers usando regra 3-sigma
detectar_outliers(dados) => {
    var μ = mean(dados);
    var σ = stdev(dados);
    var limite_inferior = μ - 3 * σ;
    var limite_superior = μ + 3 * σ;

    print("Limites: [", limite_inferior, ",", limite_superior, "]");

    for valor in dados {
        ? valor < limite_inferior or valor > limite_superior {
            print("⚠️  Outlier detectado:", valor);
        }
    }
}

var dados = [10, 12, 11, 13, 12, 100, 11, 10];  // 100 é outlier
detectar_outliers(dados);
```

---

## 📚 Referência Completa

### Palavras-chave

| Palavra | Descrição |
|---------|-----------|
| `var` | Declaração de variável |
| `for` | Loop for |
| `in` | Usado em loops for |
| `while` | Loop while |
| `?` | Condicional if |
| `otherwise` | Else |
| `return` | Retorna valor de função |
| `true` / `false` | Valores booleanos |
| `and` / `or` / `not` | Operadores lógicos |

### Tipos de Dados

- `int` - Inteiro
- `float` - Ponto flutuante
- `string` - String/texto
- `bool` - Booleano
- `array` - Array/lista

### Funções Built-in

#### Matemática
- `sqrt(x)` - Raiz quadrada
- `pow(x, y)` - Potência
- `abs(x)` - Valor absoluto
- `floor(x)` - Arredonda para baixo
- `ceil(x)` - Arredonda para cima
- `round(x)` - Arredondamento padrão

#### Estatística
- `sum(arr)` / `Σ(arr)` - Soma
- `mean(arr)` / `μ(arr)` - Média
- `median(arr)` - Mediana
- `mode(arr)` - Moda
- `stdev(arr)` / `σ(arr)` - Desvio padrão
- `variance(arr)` - Variância
- `min(arr)` - Mínimo
- `max(arr)` - Máximo

#### Utilitários
- `print(...)` - Imprime valores
- `len(arr)` - Tamanho do array
- `range(start, end)` - Cria range

---

## 🎓 Casos de Uso

Shark é ideal para:

- 📊 **Análise de dados** estatísticos
- 🔬 **Pesquisa científica** com cálculos matemáticos
- 📈 **Visualização de dados** (processamento)
- 🎲 **Simulações** estatísticas
- 🧮 **Ensino** de estatística e programação
- 📉 **Análise financeira** básica
- 🧪 **Prototipagem rápida** de algoritmos matem