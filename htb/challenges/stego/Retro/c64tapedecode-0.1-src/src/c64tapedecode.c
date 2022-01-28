/*
 * c64tapedecode.c, extract files from a C64 tape
 * Copyright (C) 2010 Christopher Williams
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "commonio.h"
#include "filter.h"
#include "packet.h"
#include "messages.h"

/* file structures:
 *   PRG:
 *     HEADER:
 *       8988 8786 8584 8382 81tt slsh eleh nnnn
 *       nnnn nnnn nnnn nnnn nnnn nnnn nnnn 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 32cs
 *       
 *       tt = type (01 = BASIC program, 03 = PRG)
 *       sl sh = start address
 *       el eh = end address + 1  (size = e-s)
 *       nn = (filename, padded to 16 bytes with \240) |
 *             tr '\040\240' '\240\040'
 *       cs = checksum (byte 10 xor byte 11 xor ... byte n-1)
 *       remaining 171 character 32's optionally contain tape loader code
 *       
 *     HEADER-REPEATED (same as header with bit 7 cleared
 *      on first 9 bytes)
 *     
 *     PAYLOAD:
 *       8988 8786 8584 8382 81xx dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       ...
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd ddcs
 *       
 *       xx = unknown
 *       dd = (e-s) bytes of file data
 *     PAYLOAD-REPEATED (same as header with bit 7 cleared
 *      on first 9 bytes)
 *   
 *   SEQ:
 *     HEADER:
 *       8988 8786 8584 8382 8104 slsh eleh nnnn
 *       nnnn nnnn nnnn nnnn nnnn nnnn nnnn 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 3232 3232 3232 3232
 *       3232 3232 3232 3232 32cs
 *
 *       similar to PRG HEADER
 *       sl sh = start address?
 *       el eh = end address + 1?
 *
 *     HEADER-REPEATED
 *     
 *     PAYLOAD:
 *       8988 8786 8584 8382 8102 dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd dddd dddd dddd dddd
 *       dddd dddd dddd dddd ddcs
 *       
 *       dd = 197 bytes of data
 *
 *     PAYLOAD-REPEATED
 *     
 *     repeat PAYLOAD and PAYLOAD-REPEATED until file
 *      is complete
 */

#define SAMPLE_RATE 44100L
#define MIN_SPEED 0.01
#define MAX_SPEED 100.

char packet_header[9] = { 0x89,0x88,0x87,0x86,0x85,0x84,0x83,0x82,0x81 };
char repeat_header[9] = { 0x09,0x08,0x07,0x06,0x05,0x04,0x03,0x02,0x01 };

char *argv0 = NULL;
int invert_samples = 0;
int keep_errors = 0;
int output_tap = 0;
int input_tap = 0;
int tap_version = 0;
long tap_size = 0;
long sample_rate = SAMPLE_RATE;

enum verbosity verbosity = VERBOSE_NORMAL;

enum filetype {
	FILE_NONE,
	FILE_BASIC,
	FILE_PRG,
	FILE_SEQ,
};

const char *filetype_names[] = {
	"NONE",
	"BASIC",
	"PRG",
	"SEQ",
};

const char spaces[] = "                ";

struct filter highpass_filter;
long highpass_freq = 0;

void usage()
{
	fprintf(stderr,
"Usage: %s [-ehprv] [-f rate] [-H freq] [-s speed]\n"
"  -e        Keep files with errors\n"
"  -f rate   Set sample rate to 'rate'\n"
"  -H freq   Apply a high-pass filter at 'freq' Hz (try -H 100).\n"
"            This can be used to remove DC offsets in the signal.\n"
"  -r        Invert samples\n"
"  -s speed  The tape was played at 'speed' times normal\n"
"  -t        Output .TAP file to standard out\n"
"  -T        Input .TAP file instead of audio\n"
"  -v        Increase verbosity level. This can be used multiple times to\n"
"            increase the amount of output printed on standard error.\n"
"  -h        Display this help message\n",
	        argv0);
}

/* assume CPU runs at 1MHz */
int tap_writepulse(FILE *file, long len)
{
	int n = len / 8 ? : 1;
	if (n > 255) {
		fprintf(file, "%c%c%c%c",
		        0, n & 0xff, (n>>8) & 0xff, (n>>16) & 0xff);
		return 4;
	} else {
		fprintf(file, "%c", n & 0xff);
		return 1;
	}
}

/* close the file and print stats about it */
static void closefile(FILE *file, char *filename, int fileerrors)
{
	if (!file) return;
	fclose(file);
	
	if (fileerrors) {
		fprintf(stderr, "\n%d errors found in \"%s\"\n",
		        fileerrors, filename);
	}
}

enum state {
	STATE_GETHEADER,
	STATE_GETPRG,
	STATE_GETSEQ,
};

int main(int argc, char *argv[])
{
	unsigned char *buf;
	int packetsize;
	int opt;
	int chksum;
	char *cbmfilename; /* CBM charset */
	char tapefilename[16+1] = ""; /* same as above but in ASCII */
	char filename[16+4+1] = ""; /* same as above but with extension */
	char fileext = 'x';
	//char *filebuf = NULL;
	//int filebufsize = 0;
	int startaddr = 0, endaddr = 0, filesize = 0;
	int i, ix;
	int type;
	float speed = 1.0;
	enum filetype filetype = FILE_NONE;
	enum state state = STATE_GETHEADER;
	FILE *outfile = NULL;
	int filenum = 0;
	int fileerrors = 0;
	int totalerrors = 0;
	FILE *tapinfile = stdin;
	FILE *tapoutfile = stdout;
	
	int getopt(int argc, char * const argv[], const char *optstring);
	
	argv0 = argv[0];
	
	while ((opt = getopt(argc, argv, "ef:H:prs:tTvh")) != -1) {
		switch (opt) {
		case 'e':
			keep_errors = 1;
			break;
		case 'f':
			sample_rate = atol(optarg);
			if (sample_rate <= 0) {
				fprintf(stderr, "%s: sample rate must be positive\n", argv0);
				return 1;
			}
			break;
		case 'H':
			highpass_freq = atol(optarg);
			break;
		case 'r':
			invert_samples = 1;
			break;
		case 's':
			speed = atof(optarg);
			if (speed < MIN_SPEED || MAX_SPEED < speed) {
				fprintf(stderr, "%s: speed must be between %f and %f\n", argv0, MIN_SPEED, MAX_SPEED);
				return 1;
			}
			break;
		case 't':
			output_tap = 1;
			break;
		case 'T':
			/* XXX: this should be detected automatically */
			input_tap = 1;
			break;
		case 'v':
			if (verbosity < VERBOSE_MAX)
				++verbosity;
			break;
		case 'h':
			usage();
			return 0;
		default: /* '?' */
			usage();
			return 1;
		}
	}
	sample_rate = sample_rate / speed;
	filter_init(&highpass_filter, highpass_freq, sample_rate);

	fprintf(stderr, " ___________________\n"
                        "|                  ||\n"
                        "|  C=64 Datasette  ||\n"
                        "|   (_)[__(_](_)   ||\n"
                        "|                  ||\n"
                        "|   ------------   ||\n"
                        "|__/._o__^__o_.\\\\__||\n");
	
	static const char tapmagic[12] = "C64-TAPE-RAW";
	if (input_tap) {
		/* read TAP header */
		char magic[12];
		char reserved[3];
		fread(magic, 12, 1, tapinfile);
		/* validate header */
		if (memcmp(magic, tapmagic, 12)) {
			fprintf(stderr, "%s: invalid TAP file\n", argv0);
			exit(1);
		}
		tap_version = fgetc(tapinfile);
		if (tap_version != 0 && tap_version != 1) {
			fprintf(stderr, "%s: unsupported TAP version (%d)\n",
			        argv0, tap_version);
			exit(1);
		}
		fread(reserved, 3, 1, tapinfile);
		tap_size = fgetlong(tapinfile);
	}
	
	if (output_tap) {
		long pulselen;
		long tapsize = 0;
		
		/* write TAP header */
		/* magic, version, reserved */
		fprintf(tapoutfile, "C64-TAPE-RAW%c%c%c%c", 1, 0, 0, 0);
		fputlong(-1L, tapoutfile); /* size */
		
		for (;;) {
			int n;
			pulselen = get_pulse(tapinfile);
			if (!pulselen) break;
			n = tap_writepulse(tapoutfile, pulselen);
			if (n < 0) break; /* on write error */
			tapsize += n;
		}
		/* patch the "Size" field of the TAP header */
		if (!fseek(tapoutfile, 0x10, SEEK_SET)) {
			fputlong(tapsize, tapoutfile);
		}
		return 0;
	}
	for (;;) {
		//fprintf(stderr, "%s %d\n", __FILE__, __LINE__);
		packetsize = get_packet(stdin, &buf);
		//fprintf(stderr, "%s %d\n", __FILE__, __LINE__);
		if (packetsize == 0) break;
		if (verbosity >= VERBOSE_PACKET) {
			fprintf(stderr, "packet size: %d\n", packetsize);
			for (i = 0; i < packetsize; ++i) {
				if ((i % 16) == 0)
					fprintf(stderr, "\n");
				fprintf(stderr, "%02x ", buf[i]);
			}
			fprintf(stderr, "\n");
		}
		if (packetsize < sizeof(packet_header) + 1) { /* too small for header */
			++fileerrors;
			state = STATE_GETHEADER;
			MESSAGE(VERBOSE_PACKET, "\nerror: packet is too small, skipping\n");
			if (verbosity == VERBOSE_FILE) fputc('S', stderr);
			continue;
		}
		if (!memcmp(buf, packet_header, sizeof(packet_header))) {
			/* first copy of packet */
			MESSAGE(VERBOSE_PACKET, "packet is first copy\n");
		} else if (!memcmp(buf, repeat_header, sizeof(repeat_header))) {
			/* repeat copy of packet */
			MESSAGE(VERBOSE_PACKET, "packet is repeated copy, skipping for now\n");
			continue; /* TODO: verify first copy with this */
		} else {
			/* packet header error */
			++fileerrors;
			MESSAGE(VERBOSE_PACKET, "\nerror: packet lacks proper header, skipping\n");
			if (verbosity == VERBOSE_FILE) fputc('H', stderr);
			continue;
		}
		
		chksum = 0;
		for (i = 9; i < packetsize-1; ++i) chksum ^= buf[i];
		if (chksum != buf[packetsize-1]) { /* bad checksum */
			++fileerrors;
			MESSAGE(VERBOSE_PACKET, "error: packet has bad checksum (0x%02x, expecting 0x%02x), skipping\n", buf[packetsize-1], chksum);
			if (verbosity == VERBOSE_FILE) fputc('C', stderr);
			//continue;
		}
		
		if (state == STATE_GETPRG) {
			state = STATE_GETHEADER;
			MESSAGE(VERBOSE_PACKET, "PRG or BASIC file contents\n");
			if (packetsize - 10 != filesize) {
				++fileerrors;
				MESSAGE(VERBOSE_FILE, "file is the wrong size (%d, expected %d)\n", packetsize - 10, filesize);
				continue;
			}
			if (verbosity == VERBOSE_FILE) fputc('.', stderr);
			if (outfile) {
				fprintf(outfile, "%c%c", startaddr%256,startaddr/256);
				fwrite(&buf[9], 1, filesize, outfile);
			}
			continue;
		}
		
		MESSAGE(VERBOSE_PACKET, "packet type: ");
		type = buf[9];
		switch (type) { /* packet type */
		case 0x01: case 0x03: case 0x04: /* BASIC or PRG, or SEQ */
			if (type == 0x01) {
				filetype = FILE_BASIC;
			} else if (type == 0x03) {
				filetype = FILE_PRG;
			} else {
				filetype = FILE_SEQ;
			}
			
			MESSAGE(VERBOSE_PACKET, "%s\n", filetype_names[filetype]);
			
			closefile(outfile, tapefilename, fileerrors);
			outfile = NULL;
			
			if (packetsize != 202) { /* wrong size */
				/* we should probably allow different size packets anyway */
				//++fileerrors;
				++totalerrors;
				MESSAGE(VERBOSE_PACKET, "error: packet is wrong size, skipping\n");
				if (verbosity == VERBOSE_FILE) fputc('s', stderr);
				continue;
			}
			startaddr = buf[10] | buf[11] << 8;
			endaddr = buf[12] | buf[13] << 8;
			filesize = endaddr - startaddr;
			cbmfilename = &buf[14];
			memmove(tapefilename, cbmfilename, 16);
			ix = -1;
			char *cp, *endp;
			for (endp = cp = &tapefilename[0]; cp < &tapefilename[16]; ++cp) {
				/*
				if ((tapefilename[i] & ~'\200') == '\040')
					tapefilename[i] ^= '\200';
				*/
				if (*cp != '\x20')
					endp = cp;
				
				/* convert "high" upper case
				 * to "low" upper case */
				if ((char)193 <= *cp && *cp < (char)219)
					*cp -= 96;
				/* swap lower case and upper case */
				if ((char)97 <= *cp && *cp < (char)123)
					*cp -= 32;
				else if ((char)65 <= *cp && *cp < (char)91)
					*cp += 32;

				/* convert shift-space to space */
				if (*cp == (char)160)
					*cp = ' ';
			}
			endp[1] = '\0';
			/* found "1234567890123456" (BASIC) at 0x0801 - 0x0807 (6 bytes) */
			if (verbosity >= VERBOSE_FILE) {
				fprintf(stderr, "\nfound \"%s\"%s (%s)%s ",
				       tapefilename,
				       &spaces[strlen(tapefilename)],
				       filetype_names[filetype],
				       &spaces[strlen(filetype_names[filetype])+16-5]);
				if (filetype == FILE_SEQ)
					fprintf(stderr, "size unknown\n");
				else
					fprintf(stderr, "at 0x%04x - 0x%04x (%d bytes)\n", startaddr, endaddr, filesize);
			}
#if 0
			MESSAGE(VERBOSE_FILE,
			        "\nfound file, name: \"%s\" "
			        "start: 0x%04x, end: 0x%04x, size: %d\n",
			        tapefilename, startaddr, endaddr, filesize);
#endif
			
			if (filetype == FILE_SEQ)
				fileext = 's';
			else
				fileext = 'p';

			/* FIXME: .p00 and .s00 are different formats from .prg. See http://www.infinite-loop.at/Power20/Documentation/Power20-ReadMe/AE-File_Formats.html for details */
			sprintf(filename, "%s.%c%02d", tapefilename, fileext, filenum);
			++filenum;
			
			totalerrors += fileerrors;
			fileerrors = 0;
			outfile = fopen(filename, "wb");
			if (!outfile) {
				perror(filename);
			}
			/* P00Magic[0..7] */
			fwrite("C64File", 1, 8, outfile);
			/* OrigFName[0..16] */
			fwrite(cbmfilename, 1, 17, outfile);
			/* RecordSize (only for REL files) */
			fwrite("", 1, 1, outfile);
			
			if (filetype == FILE_BASIC || filetype == FILE_PRG) {
				state = STATE_GETPRG;
			} else if (filetype == FILE_SEQ) {
				state = STATE_GETSEQ;
			}
			break;
		case 0x02: /* SEQ data */
			MESSAGE(VERBOSE_PACKET, "SEQ data\n");
			if (state != STATE_GETSEQ) {
				++fileerrors;
				MESSAGE(VERBOSE_PACKET, "error: SEQ data without SEQ header, skipping (TODO: save to a file if keep_errors is true)\n");
				if (verbosity == VERBOSE_FILE) putc('Q', stderr);
				continue;
			}
			if (verbosity == VERBOSE_FILE) fputc('.', stderr);
			if (outfile)
				fwrite(&buf[10], 1, 191, outfile);
			continue;
			break;
		default: /* other (PRG data?) */
			MESSAGE(VERBOSE_PACKET, "bad (0x%02x), skipping\n", type);
			continue;
			break;
		}
	}
	closefile(outfile, tapefilename, fileerrors);
	totalerrors += fileerrors;
	fprintf(stderr, "\n%d errors found\n", totalerrors);
	//putc('\n', stderr);
	return 0;
}
