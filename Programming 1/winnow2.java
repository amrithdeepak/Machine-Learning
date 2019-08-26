import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays; 
import java.io.File;

public class winnow2 {

	// Variable Declarations
	public static int alpha = 2;
	public static double theta = 8.0;
	public static double[] weights;
	public static double [][] answer;
	public static String [] answer_test;
	public winnow2() {
	}
	public static void main(String[]args) throws IOException {
		housedata(); 
		bcdata();
		irisdata();
	}

	public static void housedata() throws IOException {
	    FileWriter fileWriter = new FileWriter("/Users/amrithdeepak/Downloads/winnow2/house-votes-output.txt");
	    PrintWriter printWriter = new PrintWriter(fileWriter);
		theta = 8.0;
		// reading file
		BufferedReader in
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/house-votes-84.txt"));
		String sentence = "";
		File file =new File("/Users/amrithdeepak/Downloads/house-votes-84.txt");
		// doing it again just to get length
		BufferedReader in2
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/house-votes-84.txt"));
		String tmp = in2.readLine();
		int len = tmp.split(",").length-1;
		int cnt = 0;
		double[] temp = new double[len];
		// initializing weights
		for (int i = 0; i<temp.length; i++)
			temp[i] = 1.0;
		weights = temp; 
		// populating data with values
		while((sentence = in.readLine())!=null)
		{
			String[] splitted = sentence.split(",");
			int [] housedata = new int [splitted.length];
			for (int i =0; i<splitted.length;i++) {
				if (splitted[i].equals("republican"))
					housedata[i]= 1;
				else if (splitted[i].equals("democrat"))
					housedata[i]= 0;
				else if (splitted[i].equals("y"))
					housedata[i]= 1;
				else if (splitted[i].equals("n"))
					housedata[i]= 0;
				else if (splitted[i].equals("?"))
					housedata[i]= (int) (Math.random() *2);
			}
			// determining the total weighted sum and deciding whether to demote or promote
			double dp = 0;
			for (int i =1; i<housedata.length;i++) {
				dp += housedata[i] * weights[i-1]; 
			}

			if (dp>theta && housedata[0]==0) {
				weights = demote(weights,housedata);
			}
			else if (dp<=theta && housedata[0]==1) {
				weights = promote(weights,housedata);
			}
			cnt++;
		}
		// After training, printing weights of attributes
		printWriter.println("Weights of Attributes:");
		for (int i=1; i<weights.length+1; i++) {
			printWriter.print("Attribute " + i + ": "+weights[i-1] + " ");
		}

		printWriter.println("\n");
		// Reading files for testing
		BufferedReader testbf
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/house-votes-84-test.txt"));
		String sentence2 = "";
		File file2 =new File("~/Downloads/house-votes-84.data");

		BufferedReader testbf2
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/house-votes-84-test.txt"));
		cnt = 0;
		int wrong = 0;
		int correct = 0;
		// Classifying testing data
		while((sentence2 = testbf2.readLine())!=null)
		{
			String[] splitted = sentence2.split(",");
			int [] housedata = new int [splitted.length];
			for (int i =0; i<splitted.length;i++) {
				if (splitted[i].equals("republican"))
					housedata[i]= 1;
				else if (splitted[i].equals("democrat"))
					housedata[i]= 0;
				else if (splitted[i].equals("y"))
					housedata[i]= 1;
				else if (splitted[i].equals("n"))
					housedata[i]= 0;
				else if (splitted[i].equals("?"))
					housedata[i]= (int) (Math.random() *2);
			}
			// Getting the weighted values
			double dp = 0;
			for (int i =1; i<housedata.length;i++) {
				dp += housedata[i] * weights[i-1]; 
			}
			// Choosing whether it's correct or wrong and then printing the output
			printWriter.print("Value from Winnow2 function: "+dp+", Theta Value: "+ theta +", Actual Value: "+((housedata[0]>0)? "Republican" : "Democrat") + ", Classification: " + ((dp>theta)? "Republican" : "Democrat"));
			if ( (dp>theta && housedata[0]==0)|| (dp<=theta && housedata[0]==1)) {
				wrong++;
				printWriter.println(" Incorrect");
			}
			else {
				correct++;
				printWriter.println(" Correct");
			}
		}

		printWriter.println("The total number of correct classifications are " + correct+".");
		printWriter.println("The total number of incorrect classifications are " + wrong+".");
		printWriter.close();
		System.out.println("House Votes data Complete");
	}

	// Dividing all values 1 corresponding weights by alpha
	public static double[] demote(double[]weights, int[]values) {
		double [] weights2 = new double[weights.length];
		for (int i=1; i<values.length; i++) {
			if (values[i]==1) {
				weights2[i-1] = weights[i-1]/alpha;
			}
			else {
				weights2[i-1] = weights[i-1];
			}
		}
		return weights2;
	}

	// Multiplying all values 1 corresponding weights by alpha
	public static double[] promote(double[]weights, int[]values) {
		double [] weights2 = new double[weights.length];
		for (int i=1; i<values.length; i++) {
			if (values[i]==1) {
				weights2[i-1] = weights[i-1]*alpha;
			}
			else {
				weights2[i-1] = weights[i-1];
			}
		}
		return weights2;
	}

	public static void bcdata() throws IOException {
	    FileWriter fileWriter = new FileWriter("/Users/amrithdeepak/Downloads/winnow2/bc-output.txt");
	    PrintWriter printWriter = new PrintWriter(fileWriter);
		theta = 5.0;
		// reading file
		BufferedReader in
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin.txt"));
		String sentence = "";
		File file =new File("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin.txt");

		// doing it again just to get length
		BufferedReader in2
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin.txt"));
		String tmp = in2.readLine();
		int len = tmp.split(",").length-1;

		int cnt = 0;
		double[] temp = new double[len-1];
		for (int i = 0; i<temp.length; i++)
			temp[i] = 1.0;
		// Initializing weights
		weights = temp;
		printWriter.println();

		// populating data with values
		while((sentence = in.readLine())!=null)
		{
			String[] splitted = sentence.split(",");
			int [] bcdata = new int [splitted.length -1];
			for (int i =1; i<splitted.length;i++) {
				if (splitted[i].equals("?"))
					bcdata[i-1]= (int) (Math.random() *2);

				else if (i == splitted.length -1) {
					if (Integer.parseInt(splitted[i])==4)
						bcdata[i-1]= 0;
					else
						bcdata[i-1]= 1;
				}
				else if (Integer.parseInt(splitted[i])<6)
					bcdata[i-1]= 0;
				else
					bcdata[i-1]= 1;
			}
			// determining the total weighted sum and deciding whether to demote or promote
			double dp = 0;
			for (int i =0; i<bcdata.length-1;i++) {
				dp += bcdata[i] * weights[i]; 
			}

			if (dp>theta && bcdata[bcdata.length-1]==0) {
				weights = demote_bc(weights,bcdata);
			}
			else if (dp<=theta && bcdata[bcdata.length-1]==1) {
				weights = promote_bc(weights,bcdata);
			}
			cnt++;
		}

		// After training, printing weights of attributes
		printWriter.println("Weights of Attributes:");
		for (int i=0; i<weights.length; i++) {
			printWriter.print("Attribute " + i + ": "+weights[i] + " ");
		}


		// Reading files for testing
		printWriter.println("\n");
		BufferedReader testbf
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin-test.txt"));
		String sentence2 = "";

		BufferedReader testbf2
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin-test.txt"));
		cnt = 0;
		int wrong = 0;
		int correct = 0;

		// Classifying testing data
		while((sentence2 = testbf2.readLine())!=null)
		{
			String[] splitted = sentence2.split(",");
			int [] bcdata = new int [splitted.length-1];
			for (int i =1; i<splitted.length;i++) {
				if (splitted[i].equals("?"))
					bcdata[i-1]= (int) (Math.random() *2);
				else if (i == splitted.length -1) {
					if (Integer.parseInt(splitted[i])==4)
						bcdata[i-1]= 0;
					else
						bcdata[i-1]= 1;
				}
				else if (Integer.parseInt(splitted[i])<4)
					bcdata[i-1]= 0;
				else
					bcdata[i-1]= 1;
			}

			// Calculating weights of testing data
			double dp = 0;
			for (int i =0; i<bcdata.length-1;i++) {
				dp += bcdata[i] * weights[i]; 
			}


			// Choosing whether it's correct or wrong and then printing the output
			printWriter.print("Value from Winnow2 function: "+dp+", Theta Value: "+ theta +", Actual Value: "+((bcdata[bcdata.length-1]>0)? "malignant" : "benign") + ", Classification: " + ((dp>theta)? "malignant" : "benign"));
			if ( (dp>theta && bcdata[0]==0)|| (dp<=theta && bcdata[0]==1)) {
				wrong++;
				printWriter.println(" Incorrect");
			}
			else {
				correct++;
				printWriter.println(" Correct");
			}
		}

		printWriter.println("The total number of correct classifications are " + correct+".");
		printWriter.println("The total number of incorrect classifications are " + wrong+".");
		printWriter.close();

		System.out.println("Breast Cancer data Complete");
	}

	// Dividing all values 1 corresponding weights by alpha. 
	// Same function for iris since variable is at end.
	public static double[] demote_bc(double[]weights, int[]values) {
		double [] weights2 = new double[weights.length];
		for (int i=0; i<values.length-1; i++) {
			if (values[i]==1) {
				weights2[i] = weights[i]/alpha;
			}
			else {
				weights2[i] = weights[i];
			}
		}
		return weights2;
	}

	// Multiplying all values 1 corresponding weights by alpha
	// Same function for iris since variable is at end.
	public static double[] promote_bc(double[]weights, int[]values) {
		double [] weights2 = new double[weights.length];
		for (int i=0; i<values.length-1; i++) {
			if (values[i]==1) {
				weights2[i] = weights[i]*alpha;
			}
			else {
				weights2[i] = weights[i];
			}
		}
		return weights2;
	}

	public static void irisdata() throws IOException {
	    FileWriter fileWriter = new FileWriter("/Users/amrithdeepak/Downloads/winnow2/iris-output.txt");
	    PrintWriter printWriter = new PrintWriter(fileWriter);
		int scount =0;
		int vecount = 0;
		int vicount=0;
		String classoftest="";
		theta = 2.0;
		// Reading file
		BufferedReader in
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris.txt"));
		String sentence = "";
		// Reading file for size
		File file =new File("/Users/amrithdeepak/Downloads/iris.txt");
		int size = (int) file.length();
		answer_test = new String [size];
		BufferedReader in2
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris.txt"));
		String tmp = in2.readLine();
		int len = tmp.split(",").length-1;
		// answer is a 2D array with both the weights and the classes.
		answer = new double[3][len];
		int cnt = 0;
		double[] temp = new double[len];
		// Initializing weights
		for (int i = 0; i<temp.length; i++)
			temp[i] = 1.0;
		weights = temp; 

		// looping for each class
		for (int j =0; j<3; j++) {
			BufferedReader in3
			= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris.txt"));
			in = in3;
			switch(j)
			{
			case 0 :
				classoftest = "Iris-setosa";
			case 1 : 
				classoftest = "Iris-versicolor";
			case 2 : 
				classoftest = "Iris-virginica";

			} 
			
			// populating data with values
			while((sentence = in.readLine())!=null)
			{
				String[] splitted = sentence.split(",");
				int [] irisdata = new int [splitted.length];
				for (int i =0; i<splitted.length;i++) {
					if (i ==splitted.length-1) {
						if (splitted[i].equals(classoftest))
							irisdata[i]= 1;
						else
							irisdata[i]= 0;
					}
					// Comparing to each columns means
					else if ((i==0 &&Float.parseFloat(splitted[i])>5.84) ||(i==1 &&Float.parseFloat(splitted[i])>3.05)||(i==2 &&Float.parseFloat(splitted[i])>3.76) ||(i==3 &&Float.parseFloat(splitted[i])>1.20) )
						irisdata[i]= 1;
					else
						irisdata[i]= 0;
				}
				// Calculating weights and deciding to demote or promote
				double dp = 0;
				for (int i =0; i<irisdata.length-1;i++) {
					dp += irisdata[i] * weights[i]; 
				}

				if (dp>theta && irisdata[irisdata.length-1]==0) {
					weights = demote_bc(weights,irisdata);
				}
				else if (dp<=theta && irisdata[irisdata.length-1]==1) {
					weights = promote_bc(weights,irisdata);
				}
				cnt++;
			}
			// Printing out weights of attributes
			printWriter.println("Weights of Attributes:");
			for (int i=0; i<weights.length; i++) {
				printWriter.print("Attribute " + i + ": "+weights[i] + " ");
			}

			printWriter.println("\n");

			answer[j] = weights;

		}
		
		// Reading testing data
		BufferedReader testbf
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris-test.txt"));
		String sentence2 = "";
		String sentence4 = "";

		BufferedReader testbf2
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris-test.txt"));
		cnt = 0;
		int wrong = 0;
		int correct = 0;
		
		
		BufferedReader testbf4
		= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris-test.txt"));
		int count= 0;
		// Setting variable we are comparing to 
		while((sentence4 = testbf4.readLine())!=null)
		{
			String[] splitted = sentence4.split(",");
			answer_test[count] = splitted[splitted.length-1];
			count++;
		}
		cnt = 0;
		// Doing a test for each of the 3 classes (Setosa vs not setosa
		// versicolor vs not versicolor, virginica vs not virginica) 
		while((sentence2 = testbf2.readLine())!=null)
		{
			scount =0;
			vecount=0;
			vicount=0;
			for (int j =0; j<3; j++) {
				BufferedReader in3
				= new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris.txt"));
				in = in3;
				switch(j)
				{
				case 0 :
					classoftest = "Iris-setosa";
					weights = answer[0];
				case 1 : 
					classoftest = "Iris-versicolor";
					weights = answer[1];
				case 2 : 
					classoftest = "Iris-virginica";
					weights = answer[2];

				} 
				weights = answer[j];	    
				String[] splitted = sentence2.split(",");
				int [] irisdata = new int [splitted.length];
				for (int i =0; i<splitted.length;i++) {
					if (i ==splitted.length-1) {
						if (splitted[i].equals(classoftest))
							irisdata[i]= 1;
						else
							irisdata[i]= 0;
					}

					else if ((i==0 &&Float.parseFloat(splitted[i])>5.84) ||(i==1 &&Float.parseFloat(splitted[i])>3.05)||(i==2 &&Float.parseFloat(splitted[i])>3.76) ||(i==3 &&Float.parseFloat(splitted[i])>1.20) )
						irisdata[i]= 1;
					else
						irisdata[i]= 0;
				}
				double dp = 0;
				for (int i =0; i<irisdata.length-1;i++) {
					dp += irisdata[i] * weights[i]; 
				}
				// Getting counts of each time a class is being predicted by Winnow2
				if (dp>theta) {
					if (j==0) {
						scount++;
					}
					else if (j==1) {
						vecount++;
					}
					else { 
						vicount++;
					}

				}


			}
			// Depending on counts, we choose where to classify
			String classified = "";
			if (scount>vecount) {
				if (scount>vicount) {
					classified = "Iris-setosa";
				}
				else {
					classified = "Iris-virginica";
				}
			}
			else {
				if (vecount>vicount) {
					classified = "Iris-versicolor";
				}
				else {
					classified = "Iris-virginica";
				}
			}
			// Printing out the classified and actual and calculate if it's correct or wrong.
			printWriter.println("Classifier from Winnow2 function: "+classified+ ", Actual Value: "+ answer_test[cnt] + ", Classification: " + ((classified.equals(answer_test[cnt]))? "Correct" : "Incorrect"));
			cnt ++;
			if ( classified.equals(answer_test[cnt])) {
				correct++;
			}
			else {
				wrong++;
			}

		}

		printWriter.println("The total number of correct classifications are " + correct+".");
		printWriter.println("The total number of incorrect classifications are " + wrong+".");
		printWriter.close();
		System.out.println("Iris data Complete");
	}


}
