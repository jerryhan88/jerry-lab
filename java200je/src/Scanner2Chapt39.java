import java.util.Scanner;


public class Scanner2Chapt39 {
	public static void main(String[] args) {
		String str= readString();
		char[] charStr = str.toCharArray();
		
		int count=charStr.length;
		System.out.println("length of char" + count);
		for(int i = 0 ; i <count; i++) {
			System.out.print(charStr[i]+ ":");
		}
		System.out.println();
		int num=readInt();
		System.out.println("입력된 수 : "+ num);
	}

	public static int readInt() {
		// TODO Auto-generated method stub
		
		Scanner input = new Scanner(System.in);
		return input.nextInt();
	}

	public static String readString() {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		return input.nextLine();
	}
}
