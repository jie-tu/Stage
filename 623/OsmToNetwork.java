package MyCode;

import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.network.NetworkWriter;
import org.matsim.contrib.osm.networkReader.SupersonicOsmNetworkReader;
import org.matsim.core.utils.geometry.CoordinateTransformation;
import org.matsim.core.utils.geometry.transformations.TransformationFactory;
import org.matsim.core.network.algorithms.NetworkCleaner;

public class OsmToNetwork {
    private static final String inputFile = "G:/621/ile-de-france-latest.osm.pbf";
    private static final String outputFile = "G:/620/matsim-example-project-master/matsim-example-project-master/scenarios/ile_de_france/network.xml";
    private static final CoordinateTransformation coordinateTransformation = TransformationFactory.getCoordinateTransformation("WGS84", "EPSG:2154");

    public OsmToNetwork() {
    }

    public static void main(String[] args) {
        Network network = ((SupersonicOsmNetworkReader)(new SupersonicOsmNetworkReader.Builder()).setCoordinateTransformation(coordinateTransformation).build()).read(inputFile);
        new NetworkCleaner().run(network);
        (new NetworkWriter(network)).write(outputFile);
    }
}
