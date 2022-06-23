package MyCode;

import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.Coordinate;
import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.TransportMode;
import org.matsim.api.core.v01.population.*;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.population.PopulationUtils;
import org.matsim.core.utils.gis.ShapeFileReader;
import org.opengis.feature.simple.SimpleFeature;

import java.nio.file.Path;
import java.nio.file.Paths;

import java.util.logging.Logger;

class ShpToPopulation{
    private Population population;
    private static final Logger logger = Logger.getLogger("CreateDemand");

    ShpToPopulation(String path){

        population = PopulationUtils.createPopulation(ConfigUtils.createConfig());

        Path sampleFolder = Paths.get(path);

        for (SimpleFeature feature : ShapeFileReader.getAllFeatures(sampleFolder.resolve("trips.shp").toString())) {
            Geometry geometry = (Geometry) feature.getDefaultGeometry();
            String id = (String) feature.getAttribute("person_id").toString();
            Long trip_index = (Long) feature.getAttribute("trip_index");

            int departure_time =0;
            int arrival_time =0;
            if (feature.getAttributes().get(5) !=null) {
                departure_time = ((Long) feature.getAttributes().get(5)).intValue();
            }
            if (feature.getAttributes().get(6) !=null) {
                arrival_time = ((Double) feature.getAttributes().get(6)).intValue();
            }

            String preceding_purpose = (String) feature.getAttribute("preceding_purpose");
            String following_purpose = (String) feature.getAttribute("following_purpose");
            String mode= (String) feature.getAttribute("mode");
            if (mode.contains("car")){
                mode = TransportMode.car;
            }


            Coordinate[] coordinates = geometry.getCoordinates();
            Coord home = new Coord(coordinates[0].getX(),coordinates[0].getY());
            Coord work = new Coord(coordinates[1].getX(),coordinates[1].getY());

            if (trip_index == 0 ){
                Person person = createPerson(id,departure_time,arrival_time, mode,home,work);
                population.addPerson(person);
            }else{
                Person person = population.getPersons().get(id);
                if (person == null ){
                    person = createPerson(id,departure_time,arrival_time, mode,home,work);
                    Plan plan = createPlan( departure_time,  arrival_time, mode,home, work);
                    person.addPlan(plan);
                    //population.addPerson(p);
                }else{
                    Plan plan = createPlan( departure_time,  arrival_time, mode,home, work);
                    person.addPlan(plan);
                }


            }
        }
    }

    Population getPopulation() {
        return this.population;
    }
    void create() {

        logger.info("Done.");
    }

    private Person createPerson(String id,int HOME_END_TIME, int WORK_END_TIME, String mode ,Coord home, Coord work) {

        // create a person by using the population's factory
        // The only required argument is an id
        Person person = population.getFactory().createPerson(Id.createPersonId(id));
        Plan plan = createPlan( HOME_END_TIME,  WORK_END_TIME, mode,home, work);
        person.addPlan(plan);
        return person;
    }

    private Plan createPlan(int HOME_END_TIME, int WORK_END_TIME, String mode , Coord home, Coord work) {

        // create a plan for home and work. Note, that activity -> leg -> activity  have to be inserted in the right
        // order.
        Plan plan = population.getFactory().createPlan();

        Activity homeActivityInTheMorning = population.getFactory().createActivityFromCoord("home", home);
        homeActivityInTheMorning.setEndTime(HOME_END_TIME);
        plan.addActivity(homeActivityInTheMorning);

        Leg toWork = population.getFactory().createLeg(mode);
        plan.addLeg(toWork);

        Activity workActivity = population.getFactory().createActivityFromCoord("work", work);
        workActivity.setEndTime(WORK_END_TIME);
        plan.addActivity(workActivity);

        return plan;
    }
}
