#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <inttypes.h>
#include <string.h>
#include <pthread.h>

typedef unsigned char byte;
byte * v;
byte * A; //2d array

byte * diagonal(int len){
  byte * A = (byte *) malloc(len * len * sizeof(byte));

  for (int i = 0;i<len;i++){
    for (int j = 0;j<len;j++){
      int offset = i * len + j;
      if (i == j)
        A[offset] = 1;
      else
        A[offset] = 0;
    }
  }

  return A;
}

int * histrogram(byte * a, int n, int vlen){
  uint64_t * POW = (uint64_t *) malloc((n+1) * sizeof(uint64_t));
  for (int i = 0; i<(n+1); i++){
    POW[i] = pow(2,i);
  }

  int * hist = (int *) malloc((vlen+1) * sizeof(int));

  uint64_t * S = (uint64_t *) malloc((n+2) * sizeof(uint64_t));
  // S - Steps. for each j bit we will have S[j+1]> step to change it
  S[0] = 0;
  for (int i = 0; i < vlen+1; i++){
    hist[i] = 0;
  }
  for (int i = 0; i < n+1; i++){
    S[i+1] = (uint64_t) pow(2,i);
    //printf("%lld-", S[i]);
  }
  //printf("\n");

  hist[0] = 1;

  uint64_t m = (uint64_t) POW[n];

  byte * v = (byte *) malloc(vlen * sizeof(byte));
  for (int i = 0; i<(vlen); i++){
    v[i] = 0;
  }

  for (uint64_t i = 0; i<m; i++){
    for (int j = 1; j<(n+1); j++){
      if (i == S[j]){
        S[j] += (uint64_t) POW[j];

        int offset = vlen * (j-1);
        int w = 0;
        for (int k = 0; k<vlen; k++){
          v[k] = a[offset + k] ^ v[k];
          w += v[k];
        }

        hist[w] ++;

        //printf("w= %i,i= %lld,j=%i,S[j]= %lld\n",w,i,j,S[j]);
        break;
      }
    }
  }

  return hist;
}

struct t_basis {
  byte * A;
  int n;
  int vlen;
};


struct t_basis readfile(char * filename){
  FILE * file;
  file = fopen( filename , "r");
  char c;

  struct t_basis basis;
  int n = 0, vlen = 0, i = 0;
  int flag = 1, flag_new_vec = 1;

  byte * mem;
  byte * memnew;
  int memsize = 1;
  mem = (byte *) malloc (memsize * sizeof(byte));

  if (file) {
    while ((c = getc(file)) != EOF){
      if ((c != '\n') && (c != '\r')){
        if (flag_new_vec){
          flag_new_vec = 0;
          n ++;
        }

        if (memsize <= i){
          memnew = (byte *) malloc (memsize * 2 * sizeof(byte));
          memcpy(memnew, mem, memsize * sizeof(byte));

          if (mem != NULL) (free(mem));
          mem = memnew;//(byte *) malloc (memsize * 2 * sizeof(byte));
          //memcpy(mem, memnew, memsize * sizeof(byte));

          memsize *= 2;

          //if (memnew != NULL) (free(memnew));
        }
        mem[i] = c - '0';
        i++;
        //putchar(c);
      } else {
        if (flag){
          flag = 0;
          vlen = i;
        }
        flag_new_vec = 1;
      }
    }
    fclose(file);
  }

  basis.A = mem;
  basis.n = n;
  basis.vlen = vlen;

  return basis;
}

int writefile(char * fileout, int n, int * hist){
  FILE * file;
  file = fopen(fileout , "w");
  for(int i = 0; i<n;i++){
    fprintf(file, "%i %i\r\n",i,hist[i]);
  }
  fclose(file);

}

int main(int argc, char *argv[]){
  int * h;
  // test with diagonal matrix
  // int length = 20;
  // A = diagonal(length);
  // h = histrogram(A,length,length);
  // for(int i=0;i<length+1;i++){
  //   printf("%i ", h[i]);
  // }
  if (argc < 3){
    printf("use: %s filein fileout\n", argv[0]);
    return 1;
  }

  printf("in: %s\nout: %s\n",argv[1], argv[2]);

  //char * fname = "E:\\Users\\shareddrivers\\YandexDisk\\proj\\core\\git\\researchClosedTasks\\test_data\\in_20_32.txt";
  //char * fout = "E:\\fileout.txt";
  //char * fname = "e:\\out.txt";
  struct t_basis basis = readfile(argv[1]);

  printf("\n#vectors= %i, len= %i\n", basis.n, basis.vlen );
  // for(int i =0;i<basis.vlen * basis.n;i++){
  //   printf("%i",basis.A[i] );
  // }
  // printf("\n");

  h = histrogram(basis.A, basis.n, basis.vlen);
  for(int i=0;i<basis.vlen+1;i++){
    printf("%i ", h[i]);
  }

  writefile(argv[2], basis.vlen + 1, h);

  if (basis.A != NULL){
    free(basis.A);
  }

  return 0;
}
