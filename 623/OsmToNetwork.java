package MyCode;

import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.network.NetworkWriter;
import org.matsim.contrib.osm.networkReader.SupersonicOsmNetworkReader;
import org.matsim.core.utils.geometry.CoordinateTransformation;
import org.matsim.core.utils.geometry.transformations.TransformationFactory;

public class OsmToNetwork {
    private static final String inputFile = "G:/621/ile-de-france-latest.osm.pbf";
    private static final String outputFile = "G:/621/matsim-network.xml.gz";
    private static final CoordinateTransformation coordinateTransformation = TransformationFactory.getCoordinateTransformation("WGS84", "EPSG:25832");

    public OsmToNetwork() {
    }

    public static void main(String[] args) {
        Network network = ((SupersonicOsmNetworkReader)(new SupersonicOsmNetworkReader.Builder()).setCoordinateTransformation(coordinateTransformation).build()).read(inputFile);
        (new NetworkWriter(network)).write(outputFile);
    }
}
