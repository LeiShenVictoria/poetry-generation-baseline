package com.jd.jnlu.nlg.model;
import com.beust.jcommander.internal.Lists;
import com.google.common.base.Preconditions;
import com.google.common.primitives.Ints;
import edu.stanford.nlp.io.IOUtils;
import org.slf4j.Logger;
import com.google.common.io.ByteStreams;
import org.slf4j.LoggerFactory;
import org.tensorflow.Graph;
import org.tensorflow.Session;
import org.tensorflow.Tensor;
import org.tensorflow.TensorFlow;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
//import java.util.logging.Logger;


public class NLGTensorflowModel {

    //private static final JN
    private static final org.slf4j.Logger LOGGER = LoggerFactory.getLogger(NLGTensorflowModel.class);

    private final Graph graph;
    private final Session session;
    public NLGTensorflowModel(String modelPath) throws IOException{

        Preconditions.checkNotNull(modelPath);
        TensorFlow.loadLibrary("/home/sunbing/anaconda3/envs/python27/lib/python2.7/site-packages/tensorflow/contrib/seq2seq/python/ops/_beam_search_ops.so");
        //byte[] ops = TensorFlow.loadLibrary("/Library/Python/2.7/site-packages/tensorflow/contrib/seq2seq/python/ops/_beam_search_ops.so");

        LOGGER.info("Loading model: " + modelPath);

        InputStream is = IOUtils.getInputStreamFromURLOrClasspathOrFileSystem(modelPath);
        byte[] graphDef = ByteStreams.toByteArray(is);
        LOGGER.info("Graph def length: " + graphDef.length);

        this.graph = new Graph();
        this.graph.importGraphDef(graphDef);
        this.session = new Session(graph);

        LOGGER.info("Created baike intent tensorflow model!");

    }

    private Tensor createTensor2d(int [] data) {
        int[][] rst = new int[1][];
        rst[0] = data;
        return Tensor.create(rst);
    }

    private Tensor createTensor1d(int [] data) {
        return Tensor.create(data);
    }
    public static void Transpose(double [][]Matrix,int Line,int List,double[][]MatrixC){
        for(int i=0;i<Line;i++)
        {
            for(int j=0;j<List;j++)
            {
                MatrixC[j][i]=Matrix[i][j];
            }
        }
    }

    public int[][] predict(DataEntry dataEntry){

        Tensor inp_source =createTensor2d(dataEntry.source);
        Tensor inp_source_len =createTensor1d(dataEntry.sourceLen);

        Tensor tensor=session.runner()
                .feed("encoder_inputs",inp_source)
                .feed("encoder_inputs_length",inp_source_len)
                .fetch("decoder/out_put0000")
                .run().get(0);
        long num = tensor.shape()[1];
        long num_len=tensor.shape()[2];
        int index=(int)(Math.random()*num_len);
        int [][][] matrix = new int[1][(int)num][(int)num_len];
        int[][] matrix_2=new int[(int)num][(int)num_len];
        double[][] MatrixC=new double[(int)num_len][(int)num];
        try{
            tensor.copyTo(matrix);
        } catch (Exception e){
            return null;
        }finally {
            tensor.close();
        }
        matrix_2=matrix[0];
        //Transpose(matrix_2,(int)num,(int)num_len,MatrixC);
        return matrix_2;
    }



}

