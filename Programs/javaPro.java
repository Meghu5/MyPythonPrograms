import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.stream.Collector;
import java.util.stream.Collectors;
import java.lang.reflect.Array;
import java.util.*;

public class javaPro {

    public static boolean isPalindrome(String str) {
if (str == null || str.length() == 0) {
            return false; // An empty string or null is considered a palindrome so true or false based on your definition
        }
        String lowerStr = str.toLowerCase(); // Convert the string to lowercase for case-insensitive comparison
String cleanedStr = lowerStr.replaceAll("[^a-z0-9]", ""); // Remove non-alphanumeric characters
        int left = 0;
        int right = cleanedStr.length() - 1; // Initialize pointers for the start and end of the string
        while (left < right) { // Compare characters from both ends
            if (cleanedStr.charAt(left) != cleanedStr.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }




    public static void main(String[] args) { 
        System.out.println(isPalindrome("racecar")); // true
        System.out.println(isPalindrome("hello")); // false
        System.out.println(isPalindrome("A man a plan a canal Panama")); // true - ignoring spaces and case
        System.out.println(isPalindrome("Was it a car or a cat I saw")); // true
        System.out.println(isPalindrome("Noon")); // true - fn working for even length strings
        System.out.println(isPalindrome("madam")); // true












}

}