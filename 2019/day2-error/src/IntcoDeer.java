public class IntcoDeer {

    public static int performStuff(int[] input) {
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
        return input[0];
    }
}
