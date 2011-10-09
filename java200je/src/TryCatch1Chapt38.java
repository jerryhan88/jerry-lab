
public class TryCatch1Chapt38 {
	public static void main(String[] args){
		String sNum="123";
		String nNum="h";
		
		try{
			int a = Integer.parseInt(sNum);
			System.out.println(a);
		}catch(NumberFormatException ee) {
			System.out.println("is it int type?");
		}catch(Exception ee) {
			System.out.println("please check again");
		}finally{
			System.out.println("I want to be operated");
		}
	}
}
