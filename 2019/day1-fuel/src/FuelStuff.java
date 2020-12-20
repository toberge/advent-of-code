import java.io.*;

public class FuelStuff {
    public static void main(String[] args) {
        int total = 0;
        try (BufferedReader reader = new BufferedReader(new FileReader(new File("day1-fuel/input")))) {
            while (reader.ready()) {
                int mass = Integer.parseInt(reader.readLine());
                int fuelRequired = mass;
                fuelRequired = Math.floorDiv(fuelRequired, 3) - 2;
                while (fuelRequired > 0) {
                    total += fuelRequired;
                    fuelRequired = Math.floorDiv(fuelRequired, 3) - 2;
                }
            }
            System.out.println(total);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
