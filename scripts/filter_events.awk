/^+ malloc/{print($2, $3, $4, $6) }
/^+ calloc/{print $2, $3, $4, $8}
/^+ realloc/{print $2, $3, $4, $5, $9}
/^+ memalign/{print $2, $3, $4, $6}
/^+ posix_memalign/{print $2, $3, $10}
/^+ valloc/{print $2, $3, $6}
/^+ free/{print $2, -$3, $4, $6}
