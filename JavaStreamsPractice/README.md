# Java Streams Practice (Java 8)

`StreamsPractice.java` is a runnable collection of examples. Each example prints
an operation name and its result. All examples use the Java standard library.

## Run

From PowerShell in this directory:

```powershell
javac StreamsPractice.java
java StreamsPractice
```

## Understand a pipeline

```java
List<Integer> result = Arrays.asList(10, 15, 20, 25).stream()
        .filter(n -> n % 2 == 0)
        .map(n -> n * 2)
        .collect(Collectors.toList());
// [20, 40]
```

1. `stream()` supplies elements from the list.
2. `filter` keeps elements that satisfy the predicate: 10 and 20.
3. `map` transforms each remaining element: 20 and 40.
4. `collect` runs the pipeline and gathers its output.

An intermediate operation returns another stream. A terminal operation produces
a result or performs an action, consuming the pipeline. The original list is not
changed by this example. Streams process data; they do not store it.

## Coverage and reading order

| Section / method | Programs and concepts |
| --- | --- |
| `sources` | Collections, arrays, `of`, `empty`, builder, concatenation, infinite iteration/generation, exclusive/inclusive ranges |
| `intermediateOperations` | Filtering, mapping, flattening object/primitive streams, deduplication, sorting, pagination, null handling, debugging with `peek` |
| `terminalOperations` | Count, min/max, match operations, first/any, all three object `reduce` forms, arrays, iteration, empty results |
| `primitiveStreams` | `IntStream`, `LongStream`, `DoubleStream`, sum, average, statistics, boxing, object/primitive conversion |
| `collectors` | Lists/sets/maps, key collisions, joining, grouping, partitioning, mapping downstream, numeric collectors, reduction, finishing, custom collectors |
| `employeePrograms` | Filtering employees, comparator chains, top earners, department averages/maxima, nested grouping |
| `interviewPrograms` | Frequencies, duplicates, second distinct largest/smallest, primes, longest/unique words, first unique character, anagrams, nested totals |
| `executionBehavior` | Lazy execution, short-circuiting, single use, explicit closing, close handlers |
| `parallelStreams` | Parallel reduction/collection, ordered output, execution modes, unordered pipelines, concurrent collectors |

This covers the major Java 8 Stream API operations and collector families.
It is a practical course, rather than an exhaustive catalog of every overload.
APIs introduced after Java 8 are outside this runnable program.

## Important distinctions

| Operations | Difference |
| --- | --- |
| `filter` / `map` | Keep selected elements / transform elements |
| `map` / `flatMap` | Produce one result per input / flatten zero or more results per input |
| `distinct` / `toSet` | Continue a stream of unique values / finish by creating a set |
| `sorted` / `forEachOrdered` | Sort values by comparison / respect the existing encounter order |
| `findFirst` / `findAny` | First in encounter order, if defined / any matching element |
| `reduce` / `collect` | Combine values using an associative operation / accumulate into a container or collector result |
| `groupingBy` / `partitioningBy` | Group by arbitrary keys / split into true and false groups |
| `orElse` / `orElseGet` | Evaluate fallback argument eagerly / call fallback supplier only when empty |
| `range(1, 5)` / `rangeClosed(1, 5)` | 1, 2, 3, 4 / 1, 2, 3, 4, 5 |
| `stream` / `parallelStream` | Initially sequential / initially parallel |

## Expected results to check

The shared numbers are `[10, 20, 30, 40, 20, 5, 15]`.

| Program | Expected result |
| --- | --- |
| Even numbers | `[10, 20, 30, 40, 20]` |
| Count / sum / min / max | `7` / `140` / `5` / `40` |
| Average | `20.0` |
| Duplicate numbers | `[20]` |
| Second largest distinct number | `30` |
| Second smallest distinct number | `10` |
| First unique character of `swiss` | `w` |
| Prime numbers 1 through 30 | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]` |
| Employee salary total | `290000` |
| Department salary averages | IT `70000.0`, HR `47500.0`, Sales `55000.0` |
| Parallel sum 1 through 1000 | `500500` |
| Elements visited before / after finding first even | `0` / `2` |

## File streams

Unlike an in-memory collection stream, a file stream owns an external resource.
Use try-with-resources to close it even if processing fails:

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

// Inside a method that declares throws IOException:
try (Stream<String> lines = Files.lines(
        Paths.get("input.txt"), StandardCharsets.UTF_8)) {
    lines.filter(line -> !line.trim().isEmpty())
         .forEach(System.out::println);
}
```

`Files.list` and `Files.walk` also return streams that should be closed.
Calling a terminal operation does not automatically call `close()`.

## Mistakes to avoid

- Streams are single use. Ask the collection for a fresh stream for each pipeline.
- Intermediate operations are lazy. Without a terminal operation, they do not process elements.
- `peek` is for observation/debugging. Do not depend on it for required work; short-circuiting and optimizations can skip visits.
- Use `collect` to build a collection. Do not modify a shared `ArrayList` from parallel `forEach`.
- Reduction needs an associative operation and a correct identity. Subtraction is not associative; zero is the identity for addition, one for multiplication.
- The three-argument reduction also needs a combiner compatible with its accumulator. Use `collect` for mutable containers.
- `toMap(key, value)` rejects duplicate keys. Supply a merge function when duplicates are possible.
- `Collectors.toList()` does not promise a particular implementation or mutability. Use `toCollection(ArrayList::new)` when you require a mutable `ArrayList`.
- `toSet` and ordinary hash maps do not promise iteration order. The examples explicitly sort or use `LinkedHashMap` where predictable output matters.
- `distinct` on custom objects uses `equals` and `hashCode`. The Employee example does not implement value equality.
- `forEach` on a parallel stream does not guarantee encounter order. Use `forEachOrdered` when ordered actions are required.
- `unordered()` removes an ordering requirement; it does not shuffle the data.
- Parallel execution is not automatically faster. Small tasks, blocking work, and ordering overhead can outweigh its benefits.
- Avoid changing the source collection during processing, and keep transformation functions free of shared mutable state.
- Bound infinite streams with a suitable short-circuiting operation. Sorting an infinite stream before limiting cannot finish.
- `Optional.get()` fails when empty. Use a fallback, `ifPresent`, or `orElseThrow` with a meaningful exception.
- Empty streams return true for `allMatch` and `noneMatch`, and false for `anyMatch`.
- The second largest example means second DISTINCT value. Remove `distinct()` only when repeated values should count as separate ranks.
- Integer calculations can overflow. Choose appropriate numeric types for your real input.
- The anagram example is case-sensitive and compares Unicode code points; it does not normalize Unicode or ignore whitespace.

## Exercises

1. Find all numbers divisible by both 3 and 5.
2. Find the third largest distinct number, handling fewer than three distinct values.
3. Group words by length.
4. Find the first repeated character while preserving input order.
5. Find the two highest earners in each department.
6. Produce a map from department to sorted employee names.
7. Count words in a UTF-8 file, ignoring case and empty tokens.
8. Change the employee data so two employees have the same name and choose a deliberate merge policy.
9. Compare sequential and parallel versions on a large CPU-bound input, checking identical results before timing them.
10. Add `equals` and `hashCode` to Employee and demonstrate `distinct` on duplicate employee records.
