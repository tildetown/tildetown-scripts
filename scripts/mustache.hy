(import [json [loads]])
(import [sys [argv stdin]])
(import [pystache [render]])

(defn slurp [filename]
  (try
    (.read (apply open [filename "r"] {"encoding" "utf-8"}))
  (catch [e Exception]
    "")))

(if (= __name__ "__main__")
  (let [[template (-> (get argv 1)
                      slurp)]
        [data (-> (.read stdin)
                   loads)]]
    (print (render template data))))
