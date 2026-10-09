import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.DoubleSummaryStatistics;
import java.util.IntSummaryStatistics;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.StringJoiner;
import java.util.TreeSet;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.stream.Collector;
import java.util.stream.Collectors;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.LongStream;
import java.util.stream.Stream;

public class StreamsPractice {
    private static final List<Integer> NUMBERS =
            Arrays.asList(10, 20, 30, 40, 20, 5, 15);
    private static final List<Employee> EMPLOYEES = Arrays.asList(
            new Employee("Asha", "IT", 60000),
            new Employee("Ben", "HR", 45000),
            new Employee("Chen", "IT", 80000),
            new Employee("Divya", "Sales", 55000),
            new Employee("Evan", "HR", 50000));

    public static void main(String[] args) {
        sources();
        intermediateOperations();
        terminalOperations();
        primitiveStreams();
        collectors();
        employeePrograms();
        interviewPrograms();
        executionBehavior();
        parallelStreams();
    }

    private static void sources() {
        section("1. Creating streams");
        show("Collection.stream", NUMBERS.stream().collect(Collectors.toList()));
        show("Stream.of", Stream.of("red", "green", "blue")
                .collect(Collectors.toList()));
        show("Arrays.stream", Arrays.stream(new int[]{2, 4, 6}).sum());
        show("Stream.empty", Stream.empty().count());
        show("Stream.builder", Stream.<String>builder().add("A").add("B")
                .build().collect(Collectors.toList()));
        show("Stream.concat", Stream.concat(Stream.of(1, 2), Stream.of(3, 4))
                .collect(Collectors.toList()));
        show("Stream.iterate + limit", Stream.iterate(1, n -> n + 2).limit(5)
                .collect(Collectors.toList()));
        show("Stream.generate + limit", Stream.generate(() -> "hello").limit(3)
                .collect(Collectors.toList()));
        show("IntStream.range", IntStream.range(1, 5).boxed()
                .collect(Collectors.toList()));
        show("IntStream.rangeClosed", IntStream.rangeClosed(1, 5).boxed()
                .collect(Collectors.toList()));
    }

    private static void intermediateOperations() {
        section("2. Intermediate operations");
        show("filter: even numbers", NUMBERS.stream().filter(n -> n % 2 == 0)
                .collect(Collectors.toList()));
        show("map: square numbers", NUMBERS.stream().map(n -> n * n)
                .collect(Collectors.toList()));
        show("distinct: remove duplicates", NUMBERS.stream().distinct()
                .collect(Collectors.toList()));
        show("sorted: ascending", NUMBERS.stream().sorted()
                .collect(Collectors.toList()));
        show("sorted: descending", NUMBERS.stream().sorted(Comparator.reverseOrder())
                .collect(Collectors.toList()));
        show("skip + limit: second page", IntStream.rangeClosed(1, 10).boxed()
                .skip(3).limit(3).collect(Collectors.toList()));
        List<List<Integer>> nested = Arrays.asList(
                Arrays.asList(1, 2), Arrays.asList(3, 4), Arrays.asList(5));
        show("flatMap: flatten lists", nested.stream().flatMap(List::stream)
                .collect(Collectors.toList()));
        show("flatMapToInt", Stream.of(new int[]{1, 2}, new int[]{3, 4})
                .flatMapToInt(Arrays::stream).sum());
        show("flatMapToLong", Stream.of(new long[]{1, 2}, new long[]{3})
                .flatMapToLong(Arrays::stream).sum());
        show("flatMapToDouble", Stream.of(new double[]{1.5}, new double[]{2.5})
                .flatMapToDouble(Arrays::stream).sum());
        show("filter nulls + map", Stream.of("java", null, "streams")
                .filter(java.util.Objects::nonNull).map(String::toUpperCase)
                .collect(Collectors.toList()));
        System.out.print("peek for debugging: ");
        List<Integer> result = Stream.of(1, 2, 3).peek(n -> System.out.print(n + " "))
                .map(n -> n * 10).collect(Collectors.toList());
        System.out.println("=> " + result);
    }

    private static void terminalOperations() {
        section("3. Terminal operations");
        show("count", NUMBERS.stream().count());
        show("min", NUMBERS.stream().min(Integer::compareTo).orElse(-1));
        show("max", NUMBERS.stream().max(Integer::compareTo).orElse(-1));
        show("anyMatch: at least one > 35", NUMBERS.stream().anyMatch(n -> n > 35));
        show("allMatch: all positive", NUMBERS.stream().allMatch(n -> n > 0));
        show("noneMatch: no negatives", NUMBERS.stream().noneMatch(n -> n < 0));
        show("findFirst: first > 15", NUMBERS.stream().filter(n -> n > 15)
                .findFirst().orElse(-1));
        show("findAny: any > 15", NUMBERS.stream().filter(n -> n > 15)
                .findAny().orElse(-1));
        show("reduce with identity: sum", NUMBERS.stream().reduce(0, Integer::sum));
        show("reduce without identity: product", Stream.of(2, 3, 4)
                .reduce((a, b) -> a * b).orElse(1));
        show("reduce with combiner: total name length", EMPLOYEES.stream()
                .reduce(0, (length, e) -> length + e.getName().length(), Integer::sum));
        String[] names = EMPLOYEES.stream().map(Employee::getName).toArray(String[]::new);
        show("toArray", Arrays.toString(names));
        System.out.print("forEach: ");
        Stream.of("A", "B", "C").forEach(s -> System.out.print(s + " "));
        System.out.println();
        Optional<Integer> empty = Stream.<Integer>empty().findFirst();
        show("Optional fallback", empty.orElse(99));
        show("Optional map", Stream.of("java").findFirst().map(String::length).orElse(0));
        show("empty allMatch", Stream.<Integer>empty().allMatch(n -> n > 0));
        show("empty anyMatch", Stream.<Integer>empty().anyMatch(n -> n > 0));
        show("empty noneMatch", Stream.<Integer>empty().noneMatch(n -> n > 0));
    }

    private static void primitiveStreams() {
        section("4. Primitive streams");
        show("mapToInt + sum", NUMBERS.stream().mapToInt(Integer::intValue).sum());
        show("average", NUMBERS.stream().mapToInt(Integer::intValue).average().orElse(0));
        IntSummaryStatistics stats = NUMBERS.stream().mapToInt(Integer::intValue)
                .summaryStatistics();
        show("summaryStatistics", stats);
        show("boxed", IntStream.of(1, 2, 3).boxed().collect(Collectors.toList()));
        show("mapToObj", IntStream.rangeClosed(1, 3).mapToObj(n -> "Item " + n)
                .collect(Collectors.toList()));
        show("asLongStream", IntStream.of(1, 2, 3).asLongStream().sum());
        show("asDoubleStream", IntStream.of(1, 2, 3).asDoubleStream().average().orElse(0));
        show("LongStream: sum 1..100", LongStream.rangeClosed(1, 100).sum());
        show("DoubleStream: sum", DoubleStream.of(1.5, 2.5, 3.0).sum());
        show("mapToLong", EMPLOYEES.stream().mapToLong(Employee::getSalary).sum());
        show("mapToDouble", EMPLOYEES.stream().mapToDouble(Employee::getSalary)
                .average().orElse(0));
        show("primitive toArray", Arrays.toString(IntStream.rangeClosed(1, 4).toArray()));
    }

    private static void collectors() {
        section("5. Collectors");
        show("toList", NUMBERS.stream().collect(Collectors.toList()));
        Set<Integer> unique = NUMBERS.stream().collect(Collectors.toSet());
        show("toSet (display sorted)", new TreeSet<>(unique));
        show("toCollection: TreeSet", NUMBERS.stream()
                .collect(Collectors.toCollection(TreeSet::new)));
        show("joining", Stream.of("Java", "Streams", "Practice")
                .collect(Collectors.joining(", ", "[", "]")));
        show("toMap: name -> salary", EMPLOYEES.stream().collect(Collectors.toMap(
                Employee::getName, Employee::getSalary, (a, b) -> a, LinkedHashMap::new)));
        show("toMap: merge duplicate keys", Stream.of("apple", "banana", "apple")
                .collect(Collectors.toMap(Function.identity(), word -> 1L,
                        Long::sum, LinkedHashMap::new)));
        show("groupingBy", EMPLOYEES.stream().collect(Collectors.groupingBy(
                Employee::getDepartment, LinkedHashMap::new, Collectors.toList())));
        show("groupingBy + counting", EMPLOYEES.stream().collect(Collectors.groupingBy(
                Employee::getDepartment, LinkedHashMap::new, Collectors.counting())));
        show("groupingBy + mapping", EMPLOYEES.stream().collect(Collectors.groupingBy(
                Employee::getDepartment, LinkedHashMap::new,
                Collectors.mapping(Employee::getName, Collectors.toList()))));
        show("partitioningBy: salary >= 55000", EMPLOYEES.stream()
                .collect(Collectors.partitioningBy(e -> e.getSalary() >= 55000,
                        Collectors.mapping(Employee::getName, Collectors.toList()))));
        show("counting", EMPLOYEES.stream().collect(Collectors.counting()));
        show("summingInt", EMPLOYEES.stream().collect(Collectors.summingInt(Employee::getSalary)));
        show("summingLong", EMPLOYEES.stream().collect(Collectors.summingLong(Employee::getSalary)));
        show("summingDouble", EMPLOYEES.stream().collect(Collectors.summingDouble(Employee::getSalary)));
        show("averagingInt", EMPLOYEES.stream().collect(Collectors.averagingInt(Employee::getSalary)));
        show("averagingLong", EMPLOYEES.stream().collect(Collectors.averagingLong(Employee::getSalary)));
        show("averagingDouble", EMPLOYEES.stream().collect(Collectors.averagingDouble(Employee::getSalary)));
        show("summarizingInt", EMPLOYEES.stream().collect(Collectors.summarizingInt(Employee::getSalary)));
        show("summarizingLong", EMPLOYEES.stream().collect(Collectors.summarizingLong(Employee::getSalary)));
        DoubleSummaryStatistics stats = EMPLOYEES.stream()
                .collect(Collectors.summarizingDouble(Employee::getSalary));
        show("summarizingDouble", stats);
        show("minBy", EMPLOYEES.stream().collect(Collectors.minBy(
                Comparator.comparingInt(Employee::getSalary))).orElseThrow(IllegalStateException::new));
        show("maxBy", EMPLOYEES.stream().collect(Collectors.maxBy(
                Comparator.comparingInt(Employee::getSalary))).orElseThrow(IllegalStateException::new));
        show("reducing downstream: department totals", EMPLOYEES.stream()
                .collect(Collectors.groupingBy(Employee::getDepartment, LinkedHashMap::new,
                        Collectors.reducing(0, Employee::getSalary, Integer::sum))));
        show("collectingAndThen", EMPLOYEES.stream().map(Employee::getName)
                .collect(Collectors.collectingAndThen(Collectors.toList(),
                        java.util.Collections::unmodifiableList)));
        List<Integer> mutableResult = NUMBERS.stream().collect(
                ArrayList::new, List::add, List::addAll);
        show("collect(supplier, accumulator, combiner)", mutableResult);
        Collector<String, StringJoiner, String> customJoining = Collector.of(
                () -> new StringJoiner(" | "), StringJoiner::add,
                StringJoiner::merge, StringJoiner::toString);
        show("Collector.of", Stream.of("A", "B", "C").collect(customJoining));
    }

    private static void employeePrograms() {
        section("6. Employee programs");
        show("IT employees above 65000", EMPLOYEES.stream()
                .filter(e -> e.getDepartment().equals("IT") && e.getSalary() > 65000)
                .map(Employee::getName).collect(Collectors.toList()));
        show("Salary descending, name ascending", EMPLOYEES.stream()
                .sorted(Comparator.comparingInt(Employee::getSalary).reversed()
                        .thenComparing(Employee::getName)).collect(Collectors.toList()));
        show("Top three earners", EMPLOYEES.stream()
                .sorted(Comparator.comparingInt(Employee::getSalary).reversed())
                .limit(3).collect(Collectors.toList()));
        show("Average salary by department", EMPLOYEES.stream().collect(Collectors.groupingBy(
                Employee::getDepartment, LinkedHashMap::new,
                Collectors.averagingInt(Employee::getSalary))));
        show("Highest paid by department", EMPLOYEES.stream().collect(Collectors.groupingBy(
                Employee::getDepartment, LinkedHashMap::new,
                Collectors.maxBy(Comparator.comparingInt(Employee::getSalary)))));
        show("Nested grouping: department then salary band", EMPLOYEES.stream()
                .collect(Collectors.groupingBy(Employee::getDepartment, LinkedHashMap::new,
                        Collectors.groupingBy(e -> e.getSalary() >= 55000 ? "HIGH" : "LOW",
                                LinkedHashMap::new,
                                Collectors.mapping(Employee::getName, Collectors.toList())))));
    }

    private static void interviewPrograms() {
        section("7. Interview programs");
        Map<Integer, Long> frequencies = NUMBERS.stream().collect(Collectors.groupingBy(
                Function.identity(), LinkedHashMap::new, Collectors.counting()));
        show("Number frequency", frequencies);
        show("Duplicate numbers", frequencies.entrySet().stream()
                .filter(e -> e.getValue() > 1).map(Map.Entry::getKey)
                .collect(Collectors.toList()));
        show("Second largest DISTINCT number", NUMBERS.stream().distinct()
                .sorted(Comparator.reverseOrder()).skip(1).findFirst().orElse(-1));
        show("Second smallest DISTINCT number", NUMBERS.stream().distinct()
                .sorted().skip(1).findFirst().orElse(-1));
        show("Even/odd partition", NUMBERS.stream()
                .collect(Collectors.partitioningBy(n -> n % 2 == 0)));
        show("Prime numbers 1..30", IntStream.rangeClosed(1, 30)
                .filter(StreamsPractice::isPrime).boxed().collect(Collectors.toList()));
        show("Longest word", Stream.of("java", "streams", "programming")
                .max(Comparator.comparingInt(String::length)).orElse(""));
        show("Unique sorted words", Stream.of("java streams java", "streams are useful")
                .flatMap(line -> Arrays.stream(line.split("\\s+")))
                .distinct().sorted().collect(Collectors.toList()));
        Map<String, Long> wordCounts = Arrays.stream("java streams java are useful".split("\\s+"))
                .collect(Collectors.groupingBy(Function.identity(), LinkedHashMap::new,
                        Collectors.counting()));
        show("Word frequency", wordCounts);
        String text = "swiss";
        Map<Integer, Long> characterCounts = text.codePoints().boxed()
                .collect(Collectors.groupingBy(Function.identity(), LinkedHashMap::new,
                        Collectors.counting()));
        Optional<String> firstUnique = characterCounts.entrySet().stream()
                .filter(e -> e.getValue() == 1)
                .map(e -> new String(Character.toChars(e.getKey()))).findFirst();
        show("First non-repeating character in swiss", firstUnique.orElse("none"));
        show("Anagrams: listen/silent", areAnagrams("listen", "silent"));
        show("Flatten order items and sum", Arrays.asList(
                Arrays.asList(10, 20), Arrays.asList(30, 40)).stream()
                .flatMap(List::stream).mapToInt(Integer::intValue).sum());
    }

    private static void executionBehavior() {
        section("8. Laziness, short-circuiting, lifecycle");
        AtomicInteger visited = new AtomicInteger();
        Stream<Integer> pipeline = Stream.of(1, 2, 3, 4).filter(n -> {
            visited.incrementAndGet();
            return n % 2 == 0;
        });
        show("Visited before terminal operation", visited.get());
        show("First even", pipeline.findFirst().orElse(-1));
        show("Visited after findFirst", visited.get());
        try {
            pipeline.count();
        } catch (IllegalStateException expected) {
            show("Reusing a consumed stream", "IllegalStateException");
        }
        try (Stream<String> closeable = Stream.of("A", "B")
                .onClose(() -> System.out.println("onClose callback executed"))) {
            show("Terminal operation does not close stream", closeable.collect(Collectors.toList()));
        }
    }

    private static void parallelStreams() {
        section("9. Parallel streams");
        show("Parallel sum", IntStream.rangeClosed(1, 1000).parallel().sum());
        show("Associative parallel reduce", IntStream.rangeClosed(1, 1000).boxed()
                .parallel().reduce(0, Integer::sum));
        show("parallelStream + collect", NUMBERS.parallelStream().map(n -> n * 2)
                .collect(Collectors.toList()));
        System.out.print("forEachOrdered: ");
        IntStream.rangeClosed(1, 5).parallel().forEachOrdered(n -> System.out.print(n + " "));
        System.out.println();
        show("isParallel", NUMBERS.parallelStream().isParallel());
        show("sequential", NUMBERS.parallelStream().sequential().isParallel());
        show("unordered distinct count", NUMBERS.parallelStream().unordered().distinct().count());
        ConcurrentMap<String, Long> counts = EMPLOYEES.parallelStream().collect(
                Collectors.groupingByConcurrent(Employee::getDepartment, Collectors.counting()));
        show("groupingByConcurrent (display sorted)", new java.util.TreeMap<>(counts));
        ConcurrentMap<String, Integer> salaries = EMPLOYEES.parallelStream().collect(
                Collectors.toConcurrentMap(Employee::getDepartment, Employee::getSalary, Integer::sum));
        show("toConcurrentMap (display sorted)", new java.util.TreeMap<>(salaries));
    }

    private static boolean isPrime(int number) {
        return number >= 2 && IntStream.rangeClosed(2, (int) Math.sqrt(number))
                .noneMatch(divisor -> number % divisor == 0);
    }

    private static boolean areAnagrams(String first, String second) {
        return Arrays.equals(first.codePoints().sorted().toArray(),
                second.codePoints().sorted().toArray());
    }

    private static void section(String title) {
        System.out.println("\n" + title);
    }

    private static void show(String label, Object value) {
        System.out.println(label + " -> " + value);
    }

    private static final class Employee {
        private final String name;
        private final String department;
        private final int salary;

        Employee(String name, String department, int salary) {
            this.name = name;
            this.department = department;
            this.salary = salary;
        }

        String getName() { return name; }
        String getDepartment() { return department; }
        int getSalary() { return salary; }

        @Override
        public String toString() {
            return name + " (" + department + ", " + salary + ")";
        }
    }
}
