package MyCode;

import org.matsim.api.core.v01.population.Population;
import org.matsim.api.core.v01.population.PopulationWriter;

import java.nio.file.Paths;

public class RunShpToPopulation {

    public static void main(String[] args) {

        ShpToPopulation shpToPopulation = new ShpToPopulation("G:/621/ile-de-france/output");
        shpToPopulation.create();
        Population result = shpToPopulation.getPopulation();

        new PopulationWriter(result).write(Paths.get("G:/620/matsim-example-project-master/matsim-example-project-master/scenarios/ile_de_france/plans100.xml").toString());
    }
}

