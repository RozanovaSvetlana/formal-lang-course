## Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of boolean
  | List of string, int, boolean, double

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)

lambda =
    Lambda of List<var> * expr  // а здесь пространство для творчества
```

## Описание конкретного синтаксиса языка

 ```
 program -> stmt* EOF;
 
 stmt -> 
        | var = expr 
        | print(expr)

INT -> [0-9]+
STRING -> ([A-Z]* | [a-z]* | [0-9]* | _ | / | . )+
BOOLEAN -> True | False
 
var -> STRING
val ->
    | INT
    | STRING
    | BOOL
    | LIST<INT>
    | LIST<STRING>
    | LIST<BOOL>
    
set ->
    | SET<INT>
    | SET<STRING>
    
expr ->
    | VERTEXES
    | EDGES
    | LABELS
    | GRAPH
    | Set_start(SET, GRAPH) // задать множество стартовых состояний
    | Set_final(SET, GRAPH) // задать множество финальных состояний
    | Add_start(SET, GRAPH) // добавить состояния в множество стартовых
    | Add_final(SET, GRAPH) // добавить состояния в множество финальных
    | Get_start(GRAPH)            // получить множество стартовых состояний
    | Get_final(GRAPH)            // получить множество финальных состояний
    | Get_reachable(GRAPH)        // получить все пары достижимых вершин
    | Get_vertices(GRAPH)         // получить все вершины
    | Get_edges(GRAPH)            // получить все рёбра
    | Get_labels(GRAPH)           // получить все метки
    | Map(LAMBDA, GRAPH)         // классический map
    | Filter(LAMBDA, GRAPH)      // классический filter
    | Load(STRING)                 // загрузка графа
    | Intersect(GRAPH, GRAPH)     // пересечение языков
    | Concat(GRAPH, GRAPH)        // конкатенация языков
    | Union(GRAPH, GRAPH)         // объединение языков
    | Star(GRAPH, GRAPH)                 // замыкание языков (звезда Клини)
   
VERTEXES ->
    | SET<INT>
    | LIST<INT>

EDGES ->
    | (VERTEXES, LABEL, VERTEXES)*
    | (VERTEXES, INT, VERTEXES)*

LABELS ->
    | SET<INT>
    | SET<STRING>
    | LIST<INT>
    | LIST<STRING>

GRAPH ->
    | (SET<VERTEXES>, SET<EDGES>)

labda ->
    (LIST<VAR> -> BOOL | EXPR)
 
 ```

## Пример

Загрузить два графа с различных файлов, получить и вывести их пересечение

```
graph = Load("file_name")
graph1 = Load("second_file_name")

in = Intersect(graph, graph1)

print(in)

```

