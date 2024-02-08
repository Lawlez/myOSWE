<?php

$directoryPath = '/maps'; // Pfad zum Durchsuchen
$outputDirectory = '../output'; // Zielverzeichnis für die extrahierten Dateien
$pattern = '/\.js\.map$/'; // Regulärer Ausdruck für Dateien, die auf .js.map enden

if (!is_dir($outputDirectory)) {
    mkdir($outputDirectory, 0755, true); // Erstelle das Zielverzeichnis, falls es nicht existiert
}

$files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($directoryPath));
$jsMapFiles = [];

foreach ($files as $file) {
    if ($file->isFile() && preg_match($pattern, $file->getFilename())) {
        $jsMapFiles[] = $file->getPathname();
    }
}

foreach ($jsMapFiles as $file) {
    if (file_exists($file)) {
        $json = json_decode(file_get_contents($file));
        $directories = [];

        foreach ($json->sources as $index => $source) {
            $dir = $outputDirectory . '/' . dirname($source);
            if (!is_dir($dir)) {
                mkdir($dir, 0755, true);
            }
            $data = explode('/', $source);
            $filename = end($data);
            file_put_contents($dir . "/" . $filename, $json->sourcesContent[$index]);
            $directories[] = $dir . "/" . $filename;
        }
        print_r($directories);
    }
}
?>
