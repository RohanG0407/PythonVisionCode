package socket;
import java.io.*;
import java.net.*;
public class client {
	public static void main(String[] args) throws IOException {
		System.out.println("Console Opened");
		// TODO Auto-generated method stub
	     BufferedReader inFromUser =
	          new BufferedReader(new InputStreamReader(System.in));
	          DatagramSocket clientSocket = new DatagramSocket();
	          InetAddress IPAddress = InetAddress.getByName("10.0.20.9");
	          byte[] sendData = new byte[1024];
	          byte[] receiveData = new byte[1024];
	          String sentence = inFromUser.readLine();
	          System.out.println("sentence = " + sentence);
	          sendData = sentence.getBytes();
	          DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 9999);
	          clientSocket.send(sendPacket);
	          DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
	          clientSocket.receive(receivePacket);
	          String modifiedSentence = new String(receivePacket.getData()); //Contains angle and distance from VisionTargeting
	          System.out.println("FROM SERVER:" + modifiedSentence);
	          clientSocket.close();
              System.out.println("done");
	}

}
