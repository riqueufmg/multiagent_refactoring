package com.henrique.cleaner;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.BodyDeclaration;
import com.github.javaparser.ast.body.TypeDeclaration;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

/**
 * Main class for Java code cleaning.
 *
 * This class reads Java source code from STDIN and outputs a cleaned version to STDOUT.
 * Cleaning steps:
 * 1. Removes any top-of-file block comment (e.g., copyright or license headers).
 * 2. Removes all import statements.
 * 3. Removes all annotations from classes, methods, and fields.
 * 4. Removes all comments (single-line, block, and Javadoc) inside the code.
 * 5. Removes empty lines to compact the code.
 *
 * Inner classes, interfaces, enums, method bodies, and other code logic are preserved.
 * The cleaned output maintains package declarations and class names, allowing mirror
 * directory creation that reflects the original repository structure.
 */
public class App {

    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();

        // Read entire Java code from STDIN
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append("\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }

        String rawJava = sb.toString();
        String cleanedJava = cleanJavaCode(rawJava);

        // Output cleaned Java code to STDOUT
        System.out.println(cleanedJava);
    }

    /**
     * Cleans a Java source code string according to the rules defined in the class documentation.
     *
     * @param input The raw Java source code.
     * @return The cleaned Java code as a string.
     */
    private static String cleanJavaCode(String input) {
        try {
            // Remove any top-of-file block comment (license/copyright header)
            input = input.replaceFirst("(?s)^/\\*.*?\\*/\\s*", "");

            JavaParser parser = new JavaParser();
            ParseResult<CompilationUnit> result = parser.parse(input);

            if (!result.isSuccessful() || !result.getResult().isPresent()) {
                // Return original code if parsing fails
                return input;
            }

            CompilationUnit cu = result.getResult().get();

            // Remove all imports
            cu.getImports().clear();

            // Remove all annotations recursively
            for (TypeDeclaration<?> type : cu.getTypes()) {
                removeAnnotations(type);
            }

            // Remove all comments (single-line, block, javadoc)
            cu.getAllContainedComments().forEach(c -> c.remove());

            // Convert AST back to code
            String cleaned = cu.toString();

            // Remove empty lines
            cleaned = cleaned.replaceAll("(?m)^[ \t]*\r?\n", "");

            return cleaned;

        } catch (Exception e) {
            // Fallback: return original input on error
            return input;
        }
    }

    /**
     * Recursively removes annotations from a type declaration and its members.
     *
     * @param type The type declaration to clean.
     */
    private static void removeAnnotations(TypeDeclaration<?> type) {
        type.getAnnotations().clear();

        for (BodyDeclaration<?> member : type.getMembers()) {
            if (member.isFieldDeclaration()) {
                member.asFieldDeclaration().getAnnotations().clear();
            } else if (member.isMethodDeclaration()) {
                member.asMethodDeclaration().getAnnotations().clear();
            } else if (member.isTypeDeclaration()) {
                removeAnnotations(member.asTypeDeclaration());
            }
        }
    }
}
