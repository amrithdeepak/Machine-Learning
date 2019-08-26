import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays; 
import java.io.File;

public class naivebayes {
	
	// Variable Declarations
	public static int alpha = 2;
	public static double theta = 8.0;
	public static double[] weights;
	public static double [][] answer;
	public static String [] answer_test;
	public naivebayes() {
	}
	public static void main(String[]args) throws IOException {
		housedata();
		bcdata();
		irisdata();
	}
	
	
	public static void housedata() throws IOException {
	    FileWriter fileWriter = new FileWriter("/Users/amrithdeepak/Downloads/naivebayes/house-votes-output.txt");
	    PrintWriter printWriter = new PrintWriter(fileWriter);
		// reading files
		BufferedReader in
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/house-votes-84.txt"));
		 String sentence = "";		 
		 BufferedReader in2
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/house-votes-84.txt"));
		 String tmp = in2.readLine();
		 int len = tmp.split(",").length-1;
		 int cnt = 0;
		 int rcount = 0;
		 int dcount = 0;
		 int curr=0;
		 int num_classes=2;
		 // initializing conditional probabilities
		 double [][] conditionals = new double [num_classes][len];
		 
		 for (int i =0; i<conditionals.length;i++) {
			 for (int j =0; j<conditionals[i].length;j++) {
				 conditionals[i][j]=0.0;
			 }
		 }
		 while((sentence = in.readLine())!=null)
		 {
			 // filling in values for the array of values and
			 // the conditional counts
			 String[] splitted = sentence.split(",");
			 int [] housedata = new int [splitted.length];
			 for (int i =0; i<splitted.length;i++) {
				 if (splitted[i].equals("republican")) {
					 housedata[i]= 1;
					 curr=1;
					 rcount++;
				 }
				 else if (splitted[i].equals("democrat")) {
					 housedata[i]= 0;
					 curr = 0;
					 dcount++;
				 }
				 else if (splitted[i].equals("y")) {
					 housedata[i]= 1;
					 conditionals[curr][i-1] = conditionals[curr][i-1]+1;
					 
				 }
				 else if (splitted[i].equals("n"))
					 housedata[i]= 0;
				 else if (splitted[i].equals("?")) {
					 housedata[i]= (int) (Math.random() *2);
					 if (housedata[i]>0)
						 conditionals[curr][i-1] = conditionals[curr][i-1]+1;
				 }
			 }
		 }
		 
		 // dividing conditional counts from total count of values to get conditional probabilities
		 for (int i =0; i<conditionals[0].length;i++) {
			 conditionals[0][i] = conditionals[0][i]/((double)dcount);
			 conditionals[1][i] = conditionals[1][i]/((double)rcount);
		 }
		 
		 String sentence2 = "";
		 
		 // testing data
		 BufferedReader testbf2
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/house-votes-84-test.txt"));
		 cnt = 0;
		 int wrong = 0;
		 int correct = 0;
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

			 // Calculating Conditional Probability of classes
			 double dprob = 1.0;
			 double rprob = 1.0;
			 for (int i =1; i<housedata.length;i++) {
				 if (housedata[i] ==0) {
				    dprob *= (1-conditionals[0][i-1]);
				    rprob *= (1-conditionals[1][i-1]);
				 }
				 else {
					 dprob *= (conditionals[0][i-1]);
					 rprob *= (conditionals[1][i-1]);
				 }
			 }
			 // Calculating correct and wrong and printing values
			 printWriter.print("Conditional Probability of Democrat "+dprob+", Conditional Probability of Republican: "+ rprob +", Predicted Class: "+((housedata[0]>0)? "Republican" : "Democrat") + ", Actual Class: " + ((rprob>dprob)? "Republican" : "Democrat"));
			 if ( (rprob>dprob && housedata[0]==0)|| (rprob<=dprob && housedata[0]==1)) {
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
	
	
	
	public static void bcdata() throws IOException {
	    FileWriter fileWriter = new FileWriter("/Users/amrithdeepak/Downloads/naivebayes/bc-output.txt");
	    PrintWriter printWriter = new PrintWriter(fileWriter);
		// reading files
		BufferedReader in
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin.txt"));
		 String sentence = "";
		 
		 BufferedReader in2
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin.txt"));
		 String tmp = in2.readLine();
		 int len = tmp.split(",").length-1;
		 int cnt = 0;
		 int bcount = 0;
		 int mcount = 0;
		 int curr=0;
		 int num_classes=2;

		 // initializing conditional probabilities
		 double [][] conditionals = new double [num_classes][len-1];
		 
		 for (int i =0; i<conditionals.length;i++) {
			 for (int j =0; j<conditionals[i].length;j++) {
				 conditionals[i][j]=0.0;
			 }
		 }
		 while((sentence = in.readLine())!=null)
		 {
			 // filling in values for the array of values and
			 // the conditional counts
			 String[] splitted = sentence.split(",");
			 int [] bcdata = new int [splitted.length-1];
			 for (int i =splitted.length-1; i>0;i--) {
				 if (splitted[i].equals("?")) {
					 bcdata[i-1]= (int) (Math.random() *2);
				 	 if (bcdata[i-1]>0)
				 		 conditionals[curr][i-1] = conditionals[curr][i-1]+1;
				 }
				 else if (i == splitted.length -1) {
					 if (Integer.parseInt(splitted[i])==4) {
						 curr=0;
						 bcount++;
						 bcdata[i-1]= 0;
					 }
					 else {
						 curr = 1;
						 mcount++;
						 bcdata[i-1]= 1;
					 }
				 }
				 else if (Integer.parseInt(splitted[i])<6)
					 bcdata[i-1]= 0;
				 else {
					 bcdata[i-1]= 1;
					 conditionals[curr][i-1] = conditionals[curr][i-1]+1;
				 }
			 }
		 }
		 
		// dividing conditional counts from total count of values to get conditional probabilities
		 for (int i =0; i<conditionals[0].length;i++) {
			 conditionals[0][i] = conditionals[0][i]/((double)bcount);
			 conditionals[1][i] = conditionals[1][i]/((double)mcount);
		 }
		 
		 String sentence2 = "";
		 
		 // testing data
		 BufferedReader testbf2
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/breast-cancer-wisconsin-test.txt"));
		 cnt = 0;
		 int wrong = 0;
		 int correct = 0;
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
			// Calculating Conditional Probability of classes
			 double bprob = 1.0;
			 double mprob = 1.0;
			 for (int i =1; i<bcdata.length-1;i++) {
				 if (bcdata[i] ==0) {
				    bprob *= (1-conditionals[0][i]);
				    mprob *= (1-conditionals[1][i]);
				 }
				 else {
					 bprob *= (conditionals[0][i]);
					 mprob *= (conditionals[1][i]);
				 }
			 }

			 // Calculating correct and wrong and printing values
			 printWriter.print("Conditional Probability of Benign "+bprob+", Conditional Probability of Malignant: "+ mprob +", Predicted Class: "+((bcdata[bcdata.length-1]>0)? "Malignant" : "Benign") + ", Actual Class: " + ((mprob>bprob)? "Malignant" : "Benign"));
			 if ( (mprob>bprob && bcdata[bcdata.length-1]==0)|| (mprob<=bprob && bcdata[bcdata.length-1]==1)) {
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
	
	public static void irisdata() throws IOException {
	    FileWriter fileWriter = new FileWriter("/Users/amrithdeepak/Downloads/naivebayes/iris-output.txt");
	    PrintWriter printWriter = new PrintWriter(fileWriter);
		// reading files
		BufferedReader in
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris.txt"));
		 String sentence = "";
		 
		 BufferedReader in2
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris.txt"));
		 String tmp = in2.readLine();
		 int len = tmp.split(",").length-1;
		 int cnt = 0;
		 int scount = 0;
		 int vecount = 0;
		 int vicount = 0;
		 int curr=0;
		 int num_classes=3;
		 // initializing conditional probabilities
		 double [][] conditionals = new double [num_classes][len];
		 
		 
		 for (int i =0; i<conditionals.length;i++) {
			 for (int j =0; j<conditionals[i].length;j++) {
				 conditionals[i][j]=0.0;
			 }
		 }
		 while((sentence = in.readLine())!=null)
		 {
			// Calculating Conditional Probability of classes
			 String[] splitted = sentence.split(",");
			 int [] irisdata = new int [splitted.length];
			 for (int i =splitted.length-1; i>=0;i--) {
				 if (i == splitted.length -1) {
					 if (splitted[i].equals("Iris-setosa")) {
						 curr=0;
						 scount++;
						 irisdata[i]= 0;
					 }
					 else if (splitted[i].equals("Iris-versicolor")){
						 curr = 1;
						 vecount++;
						 irisdata[i]= 1;
					 }
					 else {
						 curr = 2;
						 vicount++;
						 irisdata[i]= 2;
					 }
				 }
				 else if ((i==0 &&Float.parseFloat(splitted[i])>5.84) ||(i==1 &&Float.parseFloat(splitted[i])>3.05)||(i==2 &&Float.parseFloat(splitted[i])>3.76) ||(i==3 &&Float.parseFloat(splitted[i])>1.20) ) {
					 irisdata[i]= 1;
					 conditionals[curr][i] = conditionals[curr][i]+1;
				 }
				 else
					 irisdata[i]= 0;
			 }
		 }
		 // dividing conditional counts from total count of values to get conditional probabilities
		 for (int i =0; i<conditionals[0].length;i++) {
			 conditionals[0][i] = conditionals[0][i]/((double)scount);
			 conditionals[1][i] = conditionals[1][i]/((double)vecount);
			 conditionals[2][i] = conditionals[2][i]/((double)vicount);
		 }
		 
		 String sentence2 = "";
		 
		 // Testing Data
		 BufferedReader testbf2
		   = new BufferedReader(new FileReader("/Users/amrithdeepak/Downloads/iris-test.txt"));
		 cnt = 0;
		 int wrong = 0;
		 int correct = 0;
		 String currclass="";
		 while((sentence2 = testbf2.readLine())!=null)
		 {
			// filling in values for the array of values and
			 // the conditional counts
			 String[] splitted = sentence2.split(",");
			 int [] irisdata = new int [splitted.length];
			 for (int i =0; i<splitted.length;i++) {
				 
				 if (i == splitted.length -1) {
					 currclass = splitted[i];
					 if (splitted[i].equals("Iris-setosa")) {
						 irisdata[i]= 0;
					 }
					 else if (splitted[i].equals("Iris-versicolor")){
						 irisdata[i]= 1;
					 }
					 else {
						 curr = 2;
						 vicount++;
						 irisdata[i]= 2;
					 }
				 }
				 else if ((i==0 &&Float.parseFloat(splitted[i])>5.84) ||(i==1 &&Float.parseFloat(splitted[i])>3.05)||(i==2 &&Float.parseFloat(splitted[i])>3.76) ||(i==3 &&Float.parseFloat(splitted[i])>1.20) ) {
					 irisdata[i]= 1;
				 }
				 else
					 irisdata[i]= 0;
			 }
			 double sprob = 1.0;
			 double veprob = 1.0;
			 double viprob = 1.0;
	 
			// Calculating Conditional Probability of classes
			 for (int i =0; i<irisdata.length-1;i++) {
				 if (irisdata[i] ==0) {
				    sprob *= (1-conditionals[0][i]);
				    veprob *= (1-conditionals[1][i]);
				    viprob *= (1-conditionals[2][i]);
				 }
				 else {
					 sprob *= (conditionals[0][i]);
					 veprob *= (conditionals[1][i]);
					 viprob *= (conditionals[2][i]);
				 }
			 }
			 // Getting class with max counts from classifier
			 int corr = 0;
			 int max = 0;
			 if (veprob>sprob) {
				 if (viprob>veprob) {
					 if (irisdata[irisdata.length-1]== 2) {
						correct++;
					 	corr=1;
					 }
					 else {
						 wrong++;
						 corr=0;
					 }
					 max = 2;
				 }
				 else {
					 if (irisdata[irisdata.length-1]== 1) {
							correct++;
							corr=1;
					 }
						 else {
							 wrong++;
							 corr=0;
						 }
					 max =1;
				 }
				 
			 }
			 
			 else {
				 if (viprob>sprob) {
					 if (irisdata[irisdata.length-1]== 2) {
							correct++;
							corr=1;
					 }
						 else {
							 wrong++;
							 corr=0;
						 }
					 max=2;
				 }
				 else {
					 if (irisdata[irisdata.length-1]== 0) {
							correct++;
							corr=1;
					 }
						 else {
							 wrong++;
							 corr=0;
						 }
				 }
			 }
			// Calculating correct and wrong and printing values
			 if (max==0) {
				 printWriter.print("Conditional Probability of Iris-Setosa "+sprob+", Conditional Probability of Iris-Versicolor: "+ veprob + ", Conditional Probability of Iris-Versicolor: " + viprob+", Predicted Class: Iris-Setosa" + ", Actual Class: " + currclass);
			 }
			 else if (max==1) {
				 printWriter.print("Conditional Probability of Iris-Setosa "+sprob+", Conditional Probability of Iris-Versicolor: "+ veprob + ", Conditional Probability of Iris-Versicolor: " + viprob+", Predicted Class: Iris-Versicolor" + ", Actual Class: " + currclass);
			 }
			 else {
				 printWriter.print("Conditional Probability of Iris-Setosa "+sprob+", Conditional Probability of Iris-Versicolor: "+ veprob + ", Conditional Probability of Iris-Versicolor: " + viprob+", Predicted Class: Iris-Virginica" + ", Actual Class: " + currclass);
		 
			 }
			 if (corr==0)
				 printWriter.println(" Incorrect");
			 else
				 printWriter.println(" Correct");
		 }
		 
		 printWriter.println("The total number of correct classifications are " + correct+".");
		 printWriter.println("The total number of incorrect classifications are " + wrong+".");

			printWriter.close();
			System.out.println("Iris data Complete");

	}
	
	
}