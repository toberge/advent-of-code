import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class ErrorHandler {
    public static void main(String[] args) {
        int[] input = null;

        try (BufferedReader reader = new BufferedReader(new FileReader(new File("day2-error/input")))) {
            String[] things = reader.readLine().split(",");
            input = new int[things.length];
            for (int i = 0; i < things.length; i++) {
                input[i] = Integer.parseInt(things[i]);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        int position = 0; // POSITION ZERO
        out:
        while (true) {
            int code = input[position];
            // of course I forgot to nest array lookups...
            switch (code) {
                case 1:
                    // addition, using pointers as specified - opcode,pos of operand,pos of operand,pos of output
                    // System.out.print("adding and replacing " + input[position + 3]);
                    input[input[position + 3]] = input[input[position + 1]] + input[input[position + 2]];
                    // System.out.println(" to " + input[position + 3] + " at " + (position + 3));
                    break;
                case 2:
                    // multiply, same syntax
                    // System.out.print("multiplying and replacing " + input[position + 3]);
                    input[input[position + 3]] = input[input[position + 1]] * input[input[position + 2]];
                    // System.out.println(" to " + input[position + 3] + " at " + (position + 3));
                    break;
                case 99:
                    // schtap
                    System.out.println("Breaking at pos " + position);
                    break out;
                default:
                    System.err.println("Gone wrongk at " + position);
                    break out;
            }
            position += 4;
        }

        System.out.println("Final state: input[0]=" + input[0]);
    }
}
