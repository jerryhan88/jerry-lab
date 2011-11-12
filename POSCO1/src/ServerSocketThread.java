
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;


public class ServerSocketThread extends Thread {
	Socket s1;
	socketServer st;
	PrintWriter pw;
	BufferedReader br;
	String name;
	String threadName = "Thread";

	public ServerSocketThread(socketServer st, Socket s1) {
		this.s1 = s1;
		this.st = st;
		threadName = getName();
		System.out.println(s1.getInetAddress() + " 님이 입장하였습니다.");
		System.out.println("Thread Name: " + threadName);
	}

	public void sendMessage(String str) {
		pw.println(str);
	}

	public void run() {
		try {
			br = new BufferedReader(new InputStreamReader(s1.getInputStream()));
			pw = new PrintWriter(s1.getOutputStream(), true);
			sendMessage("대화자 이름을 넣으세요:");
			name = br.readLine();
			st.broadCasting("[" + name + "]" + "님이 입장하였습니다.");
			while (true) {
				String strin = br.readLine();
				st.broadCasting("[" + name + "]" + strin);
			}
		} catch (Exception e) {
			System.out.println(threadName + " 퇴장했습니다.");
			st.removeClient(this);
		} finally {
			try {
				s1.close();
			} catch (Exception ex) {
				ex.printStackTrace();
			}
		}
	}
}