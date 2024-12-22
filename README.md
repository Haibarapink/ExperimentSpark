Spark 内部拥有 groupbykey 和 reducebykey 两种类似的宽依赖算子，

groupbykey+map 的操作与 reducebykey 的操作可以实现一致的操作，

reducebykey 会在每个节点先进行 combine 操作然后在 stage之间的 shuffle开销减少，使用 reducebykey 的时间应小于 groupbykey+map