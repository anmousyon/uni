//insertion sort
import java.util.*;
import java.nio.file.*;
import java.io.*;
import java.lang.Math.*;

public class insertion_sort{
    public static void main(String[] arg){
		ArrayList<Integer> input = read_list(arg[0]);
		final double start = System.nanoTime();
        input = sort(input);
        final double end = System.nanoTime();
		double time = (end-start)/1000;
		time = Math.round(time*1000)/1000;
		time /= 1000;
       	System.out.println("\nSorting took: " + time  + " ms");
		for(int x : input){
       	  	System.out.println(x);
		}
       	System.out.println("\nSorting took: " + time  + " ms");
	}

    public static ArrayList<Integer> sort(ArrayList<Integer> input){
        for(int i = 0; i < input.size(); i++){
            for(int j = i; j > 0; j--){
                if(input.get(j) < input.get(j-1)){
                    int temp = input.get(j);
                    input.set(j, input.get(j-1));
                    input.set(j-1, temp);
                }
            }
        }
        return input;
    }

    public static ArrayList<Integer> read_list(String name){
        ArrayList<Integer> input = new ArrayList<Integer>();
        try{
            for (String line : Files.readAllLines(Paths.get(name))) {
                //System.out.println(line);
                input.add(Integer.parseInt(line));
            }
        }
        catch(IOException ex){
            ex.printStackTrace();
        }
        return input;
    }
}
