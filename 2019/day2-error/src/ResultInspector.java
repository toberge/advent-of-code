import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;

/**
 * Result: 100×64+29=6429, noun=64, verb=29
 * Done through pure f-ing brute force.
 * The verb seems to always be added to the result value,
 * while the noun...
 */
public class ResultInspector {
    public static void main(String[] args) {
        int[] original, input;
        try (BufferedReader reader = new BufferedReader(new FileReader(new File("day2-error/input")))) {
            String[] things = reader.readLine().split(",");
            original = new int[things.length];
            for (int i = 0; i < things.length; i++) {
                original[i] = Integer.parseInt(things[i]);
            }
            input = Arrays.copyOf(original, original.length);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        for (int i = 0; i < 121; i++) {
            System.out.println("----- NEW SHIT -----");
            for (int j = 0; j < 121; j++) {
                System.out.println(i + ", " + j);
                input[1] = i;
                input[2] = j;
                int res = IntcoDeer.performStuff(input);
                System.out.println(res);
                if (res == 19690720) {
                    System.out.println("WE DID EEET");
                    System.exit(0);
                }
                input = Arrays.copyOf(original, original.length);
            }
        }
    }
}
